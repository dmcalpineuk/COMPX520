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

import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from SMET import map_text, map_attack_vector

file_name = './cowrie.json'
man_pages = './manpages.json'

def main():

  #map attack vectors to ATT&CK
  AV1 = 'take screenshot'
  mapping1 = map_attack_vector(AV1)

  AV2 = 'delete logs'
  mapping2 = map_attack_vector(AV2)

  AV3 = 'exfiltrate data to C2 server'
  mapping3 = map_attack_vector(AV3)

  #map any text to ATT&CK
  cve = ""
  mapping = map_text(cve,CVE = False)

  total_contents = []

  with open(file_name) as openfile:
    for line in openfile:
      total_contents.append(json.loads(line))

  with open(man_pages) as f:
    man_pages_dict = json.load(f)

  descriptions = []

  for event in total_contents:
    if 'cowrie.command.input' in event['eventid']:
      try:
        print(event['input'].split(" ", 1)[0], "-" , man_pages_dict[event['input'].split(" ", 1)[0]])
        descriptions.append(man_pages_dict[event['input'].split(" ", 1)[0]])
      except Exception:
        print(event['input'], "- unknown command")

  model = SentenceTransformer('basel/ATTACK-BERT')
  embeddings = model.encode(descriptions)

  print(cosine_similarity([embeddings[0]], [embeddings[1]]))

if __name__ == "__main__":
    main()
