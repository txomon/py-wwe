import json


def import_config(path: str):
    with open(path) as fd:
        config = json.load(fd)
    return config
