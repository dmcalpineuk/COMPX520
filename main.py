#!/usr/bin/env python3

__author__ = "Daniel McAlpine"
__copyright__ = "Copyright 2024"
__credits__ = "Junaid Haseeb, Vimal Kumar"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Daniel McAlpine"
__email__ = "contact@danielmcalpine.com"
__status__ = "Development"
__dependecies__ = "os, json, SMET, sentence_transformers"

import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
import json
from SMET import map_attack_vector


file_name = './cowrie.json'
man_pages = './manpages.json'
threshold = 0.02

def main():

  total_contents = []

  #import cowrie output from json file
  with open(file_name) as openfile:
    for line in openfile:
      total_contents.append(json.loads(line))

  #import man pages short descriptions
  with open(man_pages) as f:
    man_pages_dict = json.load(f)

  print()
  print()

  string = ""

  for event in total_contents:
    if 'cowrie.command.input' in event['eventid']:
      # Initialize a list to store the commands
      commands = []
      # Initialize a list to split the lines
      parts = []
      # Split the string on the pipe character
      parts = event['input'].split('|')
      try:
        # Iterate over the parts
        for part in parts:
          # Strip leading and trailing whitespace and split to get the first word
          next_word = part.strip().split()[0]
          commands.append(next_word)
        for command in commands:
          description = man_pages_dict[command]
          mapping = map_attack_vector(description)
          print(command, "-" , description, "-", mapping[0])
          string += description + ". "
      except Exception:
        for command in commands:
          print(command, "- unknown command")

  for event in total_contents:
    if 'cowrie.command.input' in event['eventid']:
      session_id = event['session']
      #multiples = event['input'].count('|')
      #if multiples == 0:

  print()
  print()

  print(string)
  mapping1 = map_attack_vector(string)

  print()
  print()

  print("Total mappings: ",len(mapping1))

  print()
  print()

  number = 0

  while number < len(mapping1):
    if mapping1[number][1] > threshold:
      print("- Mapping:", mapping1[number])
    number += 1

  print()
  print()
    
if __name__ == "__main__":
    main()