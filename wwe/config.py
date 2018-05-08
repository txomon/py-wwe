import json

def importConfig(path: str):
  with open(path) as fd:
    config=json.load(fd)
  return config