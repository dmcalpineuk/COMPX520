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
import re
import json
from SMET import map_attack_vector
import subprocess




file_name = './cowrie.json'
man_pages = './manpages.json'
threshold = 0.02
# Define the delimiters
delimiters = r"[ /\"\\,(\[\]{};\']+"

def main():

  total_contents = []

  #import cowrie output from json file
  with open(file_name) as openfile:
    for line in openfile:
      total_contents.append(json.loads(line))

  #import man pages short descriptions
  with open(man_pages) as f:
    man_pages_dict = json.load(f)

  string = ""

  for event in total_contents:
    if 'cowrie.command.input' in event['eventid']:
      commands = [item.strip() for item in re.split(delimiters, event['input']) if item.strip()]
      print(commands)
      for command in commands:
        try:
          description = man_pages_dict[command]
          print(type(command))
          #description = subprocess.run(['whatis', command], capture_output=True, text=True)
          mapping = map_attack_vector(description)
          print(command, "-" , description, "-", mapping[0])
          string += description + ". "
        except Exception:
          #for command in commands:
          print(command, "- unknown command")

    print()
    print()

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