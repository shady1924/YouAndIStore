from pymongo import  MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError
from django.conf import settings

class dbConnect:

    def __init__(self):
        self.__client = settings.MONGODBCLIENT

    def getClient(self):
        return self.__client
        
    def getDbConn(self, dbname):
        client = self.getClient()
        db = client[dbname]
        return db
    
    def getCollection(self,db, collection):
        return db[collection]

    def closeConnection(self):
        self.__client.close()

    def searchUpdateAndInsert(self, coll, criteria, dictObj):
        returnobj = {'result': {}, 'err': []}
        print ("Inside searchUpdateAndInsert")
        try:
            dbObj = dbConnect()
            db = dbObj.getDbConn("youandi")
            coll = dbObj.getCollection(db, coll)
            criteria = {"$and": [
                    {'monthStart': dictObj['monthStart']},
                    {'monthEnd': dictObj['monthEnd']}
                ]
            }

            result = coll.find(criteria)
            print("\n\n\n" ,"result.count()", result.count(), "col", coll, "criteria",  criteria, dictObj['monthStart'],
                  dictObj['monthEnd'])
            # Printing the results
            # for doc in result:
            #     print (doc)

            if result.count() >= 1:
                output = coll.update(criteria, dictObj)
                print("Upsert/Insert Called!!","col", coll, "criteria", output)
            else:
                output = coll.insert(dictObj)
                print("Insert Called!!", "col", coll, "criteria", output)

            returnobj["output"] = output
        except Exception as e:
            print("searchUpdateAndInsert: Error Performing DB operation", e)
            returnobj['err'].append("Error Performing database operation")
            returnobj['err'].append(e)

        return returnobj


    def updateCollection(self, collName, dictObj):
        # Insert into the database updated configuration
        dbObj = dbConnect()
        db = dbObj.getDbConn("youandi")
        coll = dbObj.getCollection(db, collName)
        insertedrec = {}

        for key, val in dictObj.items():
            output = coll.find({
                key: {"$exists": True}
            })
            print("records selected!!!", output.count())
            if output.count() >= 1:
                output = coll.update(
                    {key: {"$exists": True}},
                    {key: val}
                )
                print("updated", output)
                insertedrec[key] = output  # json.dumps(output, indent=4, sort_keys=True)
            else:
                output = coll.insert_one({key: val})
                print("inserted", output)
                if output.inserted_id:
                    insertedrec[key] = {"status": "record inserted"}
                else:
                    insertedrec[key] = {"status": "Insert Failed"}
        dbObj.closeConnection()
        return insertedrec

    def getData(self, collName, filters, projection):
        try:
            dbObj = dbConnect()
            db = dbObj.getDbConn("youandi")
            coll = dbObj.getCollection(db, collName)
            output = coll.find(filters, projection)
            print("getData: collName", collName, "filter", filters, "projection", projection)

            returnobj = {'err': []}
            # Shop Configuration information
            for doc in output:
                print("DBCOnnect : getData", doc.keys())
                # print("output",doc['monthStart'], doc['monthStart'])
                returnobj['result']=doc

        except Exception as e:
            print("getData: Error Performing DB operation", e)
            returnobj['err'].append("Error Performing database operation")
            returnobj['err'].append(e)
        return returnobj

    def getDataArr(self, collName, filters, projection):
        try:
            dbObj = dbConnect()
            db = dbObj.getDbConn("youandi")
            coll = dbObj.getCollection(db, collName)
            output = coll.find(filters, projection)
            print("collName", collName, "filter", filters, "projection", projection)
            returnobj = {'result': [] , 'err': []}
            # Shop Configuration information
            for doc in output:
                returnobj['result'].append(doc)
            # print("returnobj",returnobj)
        except Exception as e:
            print("getData: Error Performing DB operation", e)
            returnobj['err'].append("Error Performing database operation")
            returnobj['err'].append(e)
        return returnobj

    def delRecord(self, collName, filters):
        try:
            dbObj = dbConnect()
            db = dbObj.getDbConn("youandi")
            coll = dbObj.getCollection(db, collName)
            output = coll.remove(filters)
            print("collName", collName, "filter", filters)
            returnobj = {'result': [] , 'err': []}
            # Shop Configuration information
            for doc in output:
                returnobj['result'].append(doc)
            # print("returnobj",returnobj)
        except Exception as e:
            print("getData: Error Performing DB operation", e)
            returnobj['err'].append("Error Performing database operation")
            returnobj['err'].append(e)
        return returnobj