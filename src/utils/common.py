import os
from datetime import datetime
import json

def now():
    timestamp = datetime.now().timestamp()
    return timestamp

def save_json(data, dirname, filename):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    path = os.path.join(dirname, filename)
    with open(path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

def list_files_from_dir(dirname):
    files = []
    for root, _, filenames in os.walk(dirname):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass