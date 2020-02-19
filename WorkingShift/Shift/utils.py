import json
import csv
from pymongo import MongoClient

client = MongoClient()

shiftdb = client.test

workers = shiftdb.workers

bosses = shiftdb.bosses

def addBoss():
    boss = {
            "name" : "黃文松",
            "username":"Vincent",
            "password":"123"
        }
    
    bosses.insert_one(boss)

def addWorker(path):
    with open(path, 'r') as f:
        rows = csv.reader(f)
        names = [row[0] for row in rows]
        del names[0:2]
    
        for i in range(len(names)):
            workers.insert_one({
                "name":names[i],
                "id" : i,
                "email":"none@mail.example.com"
                })

def addShift(path, tablename):
    shift = shiftdb[tablename]
    with open(path, 'r') as f:
        rows = csv.reader(f)
        rows = [row for row in rows]
        date = rows[0]
        day = rows[1]
        del date[0]
        del day[0]
        data = rows[2:]
        for i in data:
            name = i[0]
            document = {
                    "name" : name,
                    "shift" : []
                    }

            for j in range(len(date)):
                document["shift"].append({
                    "date" : date[j],
                    "day" : day[j],
                    "attr" : i[j + 1]
                    })
            print(json.dumps(document, indent=4,ensure_ascii=False))
            shift.insert_one(document) 

def addRule(path, tablename):
    rule = shiftdb[tablename]
    with open(path,'r') as f:
        rows = csv.reader(f)
        rows = [row for row in rows]
        month = rows[0]
        del rows[0]
        del month[0]

        for i in range(len(rows)):
            name = rows[i][0]
            del rows[i][0]
            document = {
                    "name" : name,
                    "rules" : []
                    }
            for j in range(len(month)):
                document["rules"].append({
                        "month" : month[j],
                        "attr" : rows[i][j]
                    })
            rule.insert_one(document)

def getRule(tablename):
    rule = shiftdb[tablename]
    cursor = rule.find({})
    datas = []
    months = [rule['month'] for rule in cursor[0]['rules']]
    for data in cursor:
        del data['_id']
        datas.append(data)

    
    return {
            "months" : months,
            "data" : datas
            }
    




if __name__ == '__main__':
    getRule('rule2018')

