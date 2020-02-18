import json
from pymongo import MongoClient

client = MongoClient()

shiftdb = client.shift
workers = shiftdb.workers

if __name__ == '__main__':
    with open('./worker.json', 'r') as f:
        data = json.load(f)  
        workers.insert_one(data)

