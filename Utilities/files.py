import json


def openJSON(path):
    # Path should always contain the extension
    try:
        jsonFile = open(path)
        return json.load(jsonFile)
    except FileNotFoundError:
        return {}


def writeJSON(path, data):
    assert type(data) is dict
    oldData = openJSON(path)
    if oldData != data:
        jsonFile = open(path, "w")
        json.dump(data, jsonFile)
        print("saved {0}".format(path))
