#!/usr/bin/env python3

__author__ = "Daniel McAlpine"
__copyright__ = "Copyright 2024"
__credits__ = "Junaid Haseeb, Vimal Kumar"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Daniel McAlpine"
__email__ = "contact@danielmcalpine.com"
__status__ = "Development"
__dependecies__ = "json"

import json

file_name = './cowrie.json'
man_pages = './manpages.json'

def main():

  total_contents = []

  with open(file_name) as openfile:
    for line in openfile:
      total_contents.append(json.loads(line))

  with open(man_pages) as f:
    man_pages_dict = json.load(f)

  for event in total_contents:
    if 'cowrie.command.input' in event['eventid']:
      try:
        print(event['input'].split(" ", 1)[0], "-" , man_pages_dict[event['input'].split(" ", 1)[0]])
      except Exception:
        print(event['input'], "- unknown command")

if __name__ == "__main__":
    main()
