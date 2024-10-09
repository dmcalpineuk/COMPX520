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

import json

file_name = './cowrie_2020-02-29.json'
file_path = './cowrie.json'

def main():

  string = ''

  with open(file_name, 'r') as openfile:
    total_contents = json.load(openfile)

  for event in total_contents:
    for item in event.values():
      for next in item:
        if 'cowrie.command.input' in next['eventid']:
           string += '{"eventid":"'+next['eventid']+'","input":'+json.dumps(next['message'].split(' ', 1)[1])+',"message":'+json.dumps(next['message'])+',"sensor":"'+next['sensor']+'","timestamp":"'+next['timestamp']+'","src_ip":"'+next['src_ip_identifier']+'","session":"'+next['session_id']+'"}\n'

  with open(file_path, 'w', newline='\n') as f:
    f.writelines(string)
    

if __name__ == "__main__":
    main()
