import pymongo
import csv
from helper import *
from collections import defaultdict
from bson.objectid import ObjectId


reader = csv.reader
f = open('data.csv','rb')

conn = pymongo.MongoClient(MONGO_ADDRESS)              # Mongo Stuff
conn.admin.authenticate(MONGO_USERNAME, MONGO_PASSWORD)
db = conn.travel
collection = db.places

k = []
for i in reader(f):k.append(i)
k = k[2:]

data = defaultdict(str)

for i in range(len(k)):
    try:
        data['Orig'] = k[i][0]
        data['Orig_Flt'] = k[i][1]
        data['Arrival'] = k[i][2]
        data['Bus_Dept_BIA'] = k[i][3]
        data['Dest'] =  k[i][4]
        data['Dest_Flt'] = k[i][5]
        data['Departure'] = k[i][6]
        data['Bus_Dept_Galle'] = k[i][7]
        data['_id'] = ObjectId() #SHIt
        collection.insert_one(data)
        print i
    except:
        continue
