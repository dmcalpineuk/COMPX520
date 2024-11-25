#!/usr/bin/env python3

__author__ = "Daniel McAlpine"
__copyright__ = "Copyright 2024"
__credits__ = "Junaid Haseeb, Vimal Kumar"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Daniel McAlpine"
__email__ = "contact@danielmcalpine.com"
__status__ = "Prototype"
__dependecies__ = "json, os, platform, re, subprocess, sentence_transformers, SMET"

import json
import os
import platform
import re
import subprocess

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

#from sentence_transformers import SentenceTransformer
from SMET import map_text, map_attack_vector

#input files and location
cowrie_file = './cowrie.json'
man_pages = './manpages.json'

#output files and location
commands_file = './commands.txt'

#variables are adjustable to test outcome
threshold = 0.02
CVE = False

# Define the delimiters
primary_delimiters = r"[;&]+"
secondary_delimiters = r"[;&|({\" ,\\/]+"

def read_json_list(input_file):
  #import json file as python list
  contents = []
  with open(input_file, 'r') as openfile:
    for line in openfile:
      contents.append(json.loads(line))
  return contents

def read_json_dict(input_file):
  #import json file as python dictionary
  with open(input_file) as openfile:
    return json.load(openfile)

def write_json_list(output_data, output_file):
  #output list to json file with Unix newline
  with open(output_file, 'w', newline='\n') as openfile:
    openfile.write('\n'.join(output_data))

def write_json_dict(output_data, output_file):
  #output dictionary to json file with Unix newline
  with open(output_file, 'w', newline='\n') as openfile:
    for key in output_data.keys():
      for line in output_data[key]:
        if line is None:
          openfile.write("\n")
        else:
          openfile.write(json.dumps(line.strip())+"\n")

def get_command_description(command):
  # Run the man command and capture the output
  result = subprocess.run(
    f"man {command} | col -b",
    shell=True,
    capture_output=True,
    text=True,
    check=True
  )

  # Split the output into lines
  output = result.stdout.splitlines()

  # Initialize variables
  description_started = False
  first_sentence = ""

  for line in output:
    if re.match(r'^\s*DESCRIPTION\s*$', line, re.IGNORECASE):
      description_started = True
      continue

    if description_started:
      # Collect lines until the end of the first sentence
      first_sentence += line.strip(r'[.!?]') + " "
      if re.search(r'[.!?]', line):  # Look for sentence-ending punctuation
        break

  # Return the first sentence, trimmed of excess whitespace
  return first_sentence.strip()

def map_commands(input):
    
  description_paragraph = ''

  if platform.system() != "Linux":
    #import man pages descriptions 
    man_pages_dict = read_json_dict(man_pages)

  #map each line on first word and create paragraph
  for event in input:
    if not event:
      number = 0
      mapping = map_text(description_paragraph, CVE = CVE)
      print()
      while number < len(mapping):
        if mapping[number][1] > threshold:
          print("- Mapping:", mapping[number][0])
        number += 1
      print()
      description_paragraph = ''
    else:
      first_word = event.split()[0]
      try:
        if platform.system() == "Linux":
          #generate command from native Linux man pages
          description = get_command_description(first_word)
        else:
          description = man_pages_dict[first_word]
        mapping = map_attack_vector(description)
        print(first_word, ' - ', description, ' - ', mapping[0][0])
        description_paragraph += description + ". "
      except Exception as e:
        #print(first_word, " - No description")
        continue

def main():

  #import cowrie.json data
  total_contents = read_json_list(cowrie_file)

  print("Start")
  print()

  input = []
  new_input = []
  current_value = ""

  # create list of input events, in order, grouped by session
  for event in total_contents:
    if 'cowrie.command.input' in event['eventid']:
      primary_commands = re.split(primary_delimiters, event['input'])
      if not current_value:
        current_value = event['session']
      if current_value != event['session']:
        input.append('')
        #new_input.append('')
      for command in primary_commands:
        input.append(command.strip())
      current_value = event['session']

  for event in total_contents:
    if 'cowrie.command.input' in event['eventid']:
      secondary_commands = re.split(secondary_delimiters, event['input'])
      if not current_value:
        current_value = event['session']
      if current_value != event['session']:
        input.append('')
        #new_input.append('')
      for command in secondary_commands:
        input.append(command.strip())
      current_value = event['session']

  input.append('')
  #new_input.append('')

  #create file containing list of commands
  write_json_list(input, commands_file)

  #map_commands(input)
  #map_commands(new_input)

  for each in input:
    print(each)
#  for each in new_input:
#    print(each)

  print("End")


if __name__ == "__main__":
    main()
