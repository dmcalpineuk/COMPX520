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

#input file
file_name = './all_commands_from_log_files.json'
#output file
file_path = './test_data.json'

def main():

  string = ''

  #read contents of input file
  with open(file_name, 'r') as openfile:
    total_contents = json.load(openfile)

  #iterate through the events in input file and format to match standard cowrie output
  for next in total_contents:
    if 'cowrie.command' in next['eventid']:
      string += '{"eventid":"'+next['eventid']+'","input":'+json.dumps(next['input'])+',"message":'+json.dumps(next['message'])+',"sensor":"'+next['sensor']+'","timestamp":"'+next['timestamp']+'","src_ip":"'+next['src_ip']+'","session":"'+next['session']+'"}\n'

  #save output to file
  with open(file_path, 'w', newline='\n') as f:
    f.writelines(string)

if __name__ == "__main__":
    main()