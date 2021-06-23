import os
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

connection_string = 'mongodb+srv://mainuser:quickrate@cluster0.bbjks.mongodb.net/quickrate?retryWrites=true&w=majority'

# connection_string = os.environ.get("MONGO_DB_CONN_STR")
client = pymongo.MongoClient(connection_string)
db = client.quickrate

def get_prequote():
    cursor = db.prequote.find().sort('_id', -1).limit(10)
    return cursor

def create_prequote(quote_det, quickrate):
    data = {'quickrate': quickrate, 'quote_details': quote_det, 'created_at': datetime.now()}
    id = db.prequote.insert(data)
    cursor = db.prequote.find({'_id': id}).limit(1)
    return cursor

def delete_prequote(id):
    response = db.prequote.delete_one({'_id': ObjectId(id)})
    return response