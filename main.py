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
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import re
import json
from SMET import map_attack_vector
import subprocess
import platform


file_name = './cowrie.json'
man_pages = './manpages.json'
threshold = 0.02
# Define the delimiters
delimiters = r"[ |;\"]+"


def main():

  total_contents = []

  #import cowrie output from json file
  with open(file_name) as openfile:
    for line in openfile:
      total_contents.append(json.loads(line))

  #import man pages short descriptions
  with open(man_pages) as f:
    man_pages_dict = json.load(f)

  dictionary = {}
  count = 0

  # group events by session
  for event in total_contents:
    if 'cowrie.command.input' in event['eventid']:
      commands = [item.strip() for item in re.split(delimiters, event['input']) if item.strip()]
      if event['session'] not in dictionary.keys():
        dictionary[event['session']] = commands
      else:
        for command in commands:
          dictionary[event['session']].append(command)

  with open('temp.txt', 'w') as f:
    f.write(json.dumps(dictionary))

  for item in dictionary.keys():

    print()
    count += 1
    print("Count:",count)
    print('sessionID:', item)
    print(dictionary[item])
    print()
    
    string = ""
    
    for next in dictionary[item]:
      description = []
      try:
        if platform.system() == "Linux":
          # Run the man command and capture the output
          result = subprocess.run(
            f"man {next} | col -b",
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
          description =  first_sentence.strip()

        else:
          description = man_pages_dict[next]#.strip(r'[.]')

        mapping = map_attack_vector(description)
        print(next, "-" , description, "-", mapping[0])
        string += description + ". "

      except Exception:
        continue
        #print(next, "- unknown command")

    print()
    print()

    print(string.strip())
    mapping1 = map_attack_vector(string.strip())

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
