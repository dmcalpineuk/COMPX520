#!/usr/bin/env python3

__author__ = "Daniel McAlpine"
__copyright__ = "Copyright 2024"
__credits__ = "Junaid Haseeb, Vimal Kumar"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Daniel McAlpine"
__email__ = "contact@danielmcalpine.com"
__status__ = "Development"
__dependecies__ = "json, sentence_transformers"

import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
import json
#from sentence_transformers import SentenceTransformer
#from sklearn.metrics.pairwise import cosine_similarity
from SMET import map_attack_vector


#from transformers.utils import logging
#logging.set_verbosity_error()

file_name = './cowrie.json'
man_pages = './manpages.json'

def main():

  total_contents = []

  with open(file_name) as openfile:
    for line in openfile:
      total_contents.append(json.loads(line))

  with open(man_pages) as f:
    man_pages_dict = json.load(f)

  descriptions = []
  #model = SentenceTransformer('basel/ATTACK-BERT')
  
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
        mapping = map_attack_vector(description)
        descriptions.append(description)
        print(command, "-", description, "- Mapping:", mapping)
      except Exception:
        print(command, "- unknown command")

  print()
  print()
    
if __name__ == "__main__":
    main()