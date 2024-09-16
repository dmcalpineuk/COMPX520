#!/usr/bin/env python3

__author__ = "Daniel McAlpine"
__copyright__ = "Copyright 2024"
__credits__ = "Junaid Haseeb, Vimal Kumar"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Daniel McAlpine"
__email__ = "contact@danielmcalpine.com"
__status__ = "Development"
__dependecies__ = "json, SMET"

import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
import json
from SMET import map_attack_vector


file_name = './cowrie.json'
man_pages = './manpages.json'

def main():

  total_contents = []

  with open(file_name) as openfile:
    for line in openfile:
      total_contents.append(json.loads(line))

  with open(man_pages) as f:
    man_pages_dict = json.load(f)

  string = ""
  
  print()
  print()

  for event in total_contents:
    if 'cowrie.command.input' in event['eventid']:
      command = event['input'].split(" ", 1)[0]
      try:
        description = man_pages_dict[command]
        #embeddings = model.encode(description)
        #cs = cosine_similarity([embeddings[0]], [embeddings[1]])
        #map attack vectors to ATT&CK
        #descriptions.append(description)
        string += description + ". "
        mapping = map_attack_vector(string)
      except Exception:
        print(command, "- unknown command")

  print(string)
  number = 0
  print(len(mapping))
  while number < len(mapping):
    if mapping[number][1] > 0.02:
      print("- Mapping:", mapping[number])
    number += 1

  print()
  print()
    
if __name__ == "__main__":
    main()