import json
import csv
import calendar
import os
import subprocess
import hashlib
from pymongo import MongoClient

client = MongoClient()

shiftdb = client.test

workers = shiftdb.workers

bosses = shiftdb.bosses

MONTH = {
            "Jan" : "1",
            "Feb" : "2",
            "Mar" : "3",
            "Apr" : "4",
            "May" : "5",
            "Jun" : "6",
            "Jul" : "7",
            "Aug" : "8",
            "Sep" : "9",
            "Oct" : "10",
            "Nov" : "11",
            "Dec" : "12"
        }

month = {
            "1" : "Jan",
            "2" : "Feb",
            "3" : "Mar",
            "4" : "Apr",
            "5" : "May",
            "6" : "Jun",
            "7" : "Jul",
            "8" : "Aug",
            "9" : "Sep",
            "10" : "Oct",
            "11" : "Nov",
            "12" : "Dec"
        }

days = {
        1:"Mon",
        2:"Tue",
        3:"Wed",
        4:"Thu",
        5:"Fri",
        6:"Sat",
        7:"Sun",
        }

def md5Hash(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()

def addBoss():
    password = md5Hash("321")
    print("password ",password)
    boss = {
            "name" : "林友鈞",
            "username":"Eugene",
            "password":password
        }
    
    # bosses.insert_one(boss)

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

def getRule(query):
    try:
        year = query['year']
    except:
        return None

    tablename = 'rule' + year
    rule = shiftdb[tablename]
    cursor = rule.find({})
    try:
        datas = []
        months = [rule['month'] for rule in cursor[0]['rules']]
        for data in cursor:
            del data['_id']
            datas.append(data)
    except:
        return None
    
    return {
            "months" : months,
            "data" : datas
            }


def getShift(tablename):
    shift = shiftdb[tablename]
    cursor = shift.find({})
    datas = []
    dates = [element['date'] for element in cursor[0]['shift']]
    days = [element['day'] for element in cursor[0]['shift']]

    document = {}
    document["firstdate"] = dates[0]
    document["firstday"] = days[0]

    del dates[0]
    del days[0]
    i = 0
    # I need to seperate the below part
    # because if we create the shift, we must return shift in formal back to view.py
    # I'll update in next version
    for data in cursor:
        del data['_id']
        data["firstShift"] = data["shift"][0]
        del data["shift"][0]
        if i % 2 == 0:
            data["grey"] = True
        i += 1
        datas.append(data)

    document["date"] = dates
    document["data"] = datas
    document["day"] = days
    
    return document

def generateTheCalendarCSV(data:dict):
    keys = data.keys()
    print(keys)
    pass

def getCollection(year):
    data = []
    data.append([])
    data.append([])
    data.append([])
    data.append([])
    for i in range(1,13):
        shiftCursor= shiftdb['shift'+year+str(i)]
        dbData = shiftCursor.find_one({})
        if dbData == None:
            dbData = {'attr':False}
        else:
            dbData = {'attr':True}
        dbData['MONTH'] = month[str(i)]
        dbData['month'] = i
        dbData['year'] = year
        data[int((i - 1)/3)].append(dbData)

    print(data)
    return data

def checkYearMonthLegal(query):
    try:
        year = query['year']
        mon = query['month']
        mon = MONTH[mon]
    except:
        return

    # try to get the rule of year
    cursor = shiftdb['rule'+year]
    data = cursor.find_one({})
    if data == None:
        return
    
    # try to get the month shift
    cursor = shiftdb['shift'+year+mon]
    
    # if data == None -> create the shift
    data = cursor.find_one({})
    if data == None:
        createShift(year, mon) 
        pass
    return {'year' : year, 'month' : mon} 

def createShift(year, month):
    # generate the calendar
    year = int(year)
    month = int(month)
    cal = calendar.Calendar()
    dates = cal.itermonthdates(year, month)
    targetDate = []
    for date in dates:
        if date.month == month:
            targetDate.append(date)
    

    
    # get the Worker
    labors = workers.find({})
    # create the shift 
    workershift = []
    for worker in labors:
        w = {
                "name" : worker['name'],
                "shift" : [],
                "id" : worker['id']
            }
        if worker['name'] == '黃文松':
            for i in targetDate:
                if i.weekday() == 6 or i.weekday() == 5:
                    attr = "Z"
                else:
                    attr = "W"
                w["shift"].append({
                        "date" : i.day,
                        "day" : days[i.weekday() + 1],
                        "attr" : attr
                    })
        else:
            for i in targetDate:
                w["shift"].append({
                        "date" : i.day,
                        "day" : days[i.weekday() + 1],
                        "attr" : "W"
                    })
        workershift.append(w)

    shift = shiftdb['shift'+str(year)+str(month)]
    shift.insert_many(workershift)

def generateTheCalendarCSV(data, year, month):
    path = os.path.dirname(__file__) + '/Working-Shift-Scheduling/files/calendar' + year + MONTH[month] + '.csv'
    with open(path,'w') as f:
        writer = csv.writer(f)
        keys = data.keys()
        if int(data['Date'][1]) > int(data['Date'][2]):
            for key in keys:
                del data[key][1]
                writer.writerow(data[key])
        else:
            for key in keys:
                writer.writerow(data[key])

        
def generateNextMonthCSV(year, month):
    year = int(year)
    month = int(MONTH[month])
    path1 = os.path.dirname(__file__) + '/Working-Shift-Scheduling/files/calendar' + str(year) + str(month) + '.csv'
    month += 1
    if month > 13:
        year += 1
    month %= 13
    path2 = os.path.dirname(__file__) + '/Working-Shift-Scheduling/files/calendar' + str(year) + str(month) + '.csv'
    os.system("cp %s %s" % (path1, path2))


def generateHolidayCSV(data, year, month):
    rows = []
    rows.append(data['Date'])
    rows.append(data['Day'])
    data['黃文松'][0] = 'Holiday'
    rows.append(data['黃文松'])
    path = os.path.dirname(__file__) + '/Working-Shift-Scheduling/files/holiday' + year + MONTH[month] + '.csv'
    with open (path, 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(rows)
    pass

def executeProgram(year, month):
    month = int(MONTH[month])
    last_month = month - 1
    if last_month == 0:
        last_month = 12
    next_month = month + 1
    if next_month == 13:
        next_month = 12
    path = os.path.dirname(__file__)
    command = '%s/Working-Shift-Scheduling/objects/main -y %s -m %s %s %s -p %s/Working-Shift-Scheduling/files/' % (path,year, last_month, month, next_month, path)
    os.system(command)
    pass

def updateDataBase(year, month):
    cursor = shiftdb['shift'+year+MONTH[month]]
    path = os.path.dirname(__file__) + '/Working-Shift-Scheduling/files/shift%s%s.csv' %(year, MONTH[month])
    with open(path, 'r') as f:
        rows = csv.reader(f)
        rows = [row for row in rows]
        date = rows[0]
        day = rows[1]
        del date[0]
        del day[0]
        data = rows[2:]
        print(data)
        print(date)
        for i in data:
            name = i[0]
            document = [] 
            for j in range(len(date)):
                document.append({
                    "date" : date[j],
                    "day" : day[j],
                    "attr" : i[j + 1]
                    })
            #print(json.dumps(document, indent=4,ensure_ascii=False))
            cursor.update_one({"name" : name}, {"$set" : {"shift":document}})

    pass

def checkLogin(data):
    data['password'] = md5Hash(data['password'])
    result = bosses.find_one(data)  
    if result != None:
        return True
    else:
        return False

def uploadQuality(year, month):
    path = os.path.dirname(__file__) + '/../quality/shift%s%s.quality.csv' %(year, month)
    data = {}
    rows = []
    try:
        with open(path, 'r') as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                rows.append(row)
            
            data['header'] = rows[0]
            del rows[0]
            
            data['content'] = rows

            return data
    except:
        return

def saveShift(data, year, month):
    tablename = 'shift' + year + month
    shift = shiftdb[tablename]
    print(data)
    pass
				
if __name__ == '__main__':
    checkLogin({"username" : "Eugene", "password" : "321"})
    # addBoss()    
    # checkYearMonthLegal({'year':'2018', 'month':'Jan'})
    # createShift(2018,9)
    # cal = calendar.Calendar()
    # dates = cal.itermonthdates(2018,5)

