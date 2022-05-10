import json
import numpy as np 

def buildJson(scan_name, name, data):
    file_name = scan_name+'/'+name+'.json'
    print(file_name)
    with open(file_name, 'w') as file:
        json.dump(data, file, indent = 4)

def getJsonData(json_name):
    with open(json_name, 'r') as file:
        data =  json.load(file)
    return data