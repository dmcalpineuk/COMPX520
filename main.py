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
import SMET #from SMET import map_text, map_attack_vector

#input files and location
cowrie_file = './cowrie.json'
man_pages = './manpages.json'

#output files and location
commands_file = './commands CVE on.txt'
mapped_commands = './mapped CVE on.txt'

#variables are adjustable to test outcome
threshold = 0.1
isCVE = True

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
    
  if platform.system() != 'Linux':
    #import man pages descriptions 
    man_pages_dict = read_json_dict(man_pages)

  description_paragraph = ''
  output_list = []
  switch = True
  counter = len(input)

  #map each line on first word and create paragraph
  for event in input:
    if (switch):
      output_list.append(event)
      switch = False
      print(counter)
      counter -=1
    elif not event:
      number = 0
      mapping = SMET.map_text(description_paragraph, isCVE)
      output_list.append('')
      #output_list.append(description_paragraph)
      #output_list.append('')
      while number < len(mapping):
        if mapping[number][1] > threshold:
          output_list.append("- Mapping:" + '\t\t' + mapping[number][0])
        number += 1
      output_list.append('')
      description_paragraph = ''
      switch = True
    else:
      first_word = event.split()[0]
      try:
        if platform.system() == "Linux":
          #generate command from native Linux man pages
          description = get_command_description(first_word)
        else:
          description = man_pages_dict[first_word]
        mapping = SMET.map_attack_vector(description)
        output_list.append(event + '\t' + description + '\t' + mapping[0][0])
        description_paragraph += description + ". "
      except Exception as e:
        continue

  return output_list

def main():

  #import cowrie.json data
  total_contents = read_json_list(cowrie_file)

  input = []
  current_value = ""

  # create list of input events, in order, grouped by session
  for event in total_contents:
    if 'cowrie.command' in event['eventid']:
      if not current_value:
        current_value = event['session']
        input.append("Session ID: " + current_value.strip())
      if current_value != event['session']:
        input.append('')
        current_value = event['session']
        input.append("Session ID: " + current_value.strip())
      primary_commands = re.split(primary_delimiters, event['input'].strip())
      for command in primary_commands:
        input.append(command.strip())

  input.append('')
  current_value = ""

  for event in total_contents:
    if 'cowrie.command' in event['eventid']:
      if not current_value:
        current_value = event['session']
        input.append("Session ID: " + current_value.strip())
      if current_value != event['session']:
        input.append('')
        current_value = event['session']
        input.append("Session ID: " + current_value.strip())
      secondary_commands = re.split(secondary_delimiters, event['input'].strip())
      for command in secondary_commands:
        input.append(command.strip())
  
  input.append('')

  #create file containing list of commands
  write_json_list(input, commands_file)

  output = map_commands(input)

  for line in output:
    print(line)

  write_json_list(output, mapped_commands)

if __name__ == "__main__":
  print("Start" + '\n')
  main()
  print("End")