# test update
import pymongo

connection_string = "mongodb+srv://jovifez:lambton@cluster0.zkkwmhc.mongodb.net/test"

try:
    myClient = pymongo.MongoClient(connection_string)
    print("Connected to MongoDB successfully.")
except Exception:
    print("Error:" + Exception)
    
print(myClient.list_database_names())

db_myFirstDatabase = myClient.myFirstDatabase

#dict_list = list(db_myFirstDatabase.employee.find({"EmployeeName":"Martin"}))
#print(dict_list)


myDB = myClient["myFirstDatabase"]
myCollection = myDB["employee"]
myDoc = {
        "id_" : 0,
        "name" : "Jovi"
        }

myCollection.insert_one(myDoc)


dict_list = list(myCollection.find({"EmployeeName":"Martin"}))
print(dict_list)

for item in dict_list:
    print(item["_id"])

'''
original_id = ObjectId()
print(original_id)

db.places.insertOne({
    "_id": original_id,
    "name": "Broadway Center",
    "url": "bc.example.net"
})

db.people.insertOne({
    "name": "Erin",
    "places_id": original_id,
    "url":  "bc.example.net/Erin"
})
'''