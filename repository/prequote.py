import os
import pymongo
import time
from datetime import datetime

connection_string = os.environ.get("MONGO_DB_CONN_STR")
client = pymongo.MongoClient(connection_string)
db = client.quickrate

def get_prequote():
    response = db.prequote()
    return response

def create_prequote(quote_det, quickrate):
    data = {'quickrate': quickrate, 'quote_details': quote_det, 'created_at': datetime.now()}
    id = db.prequote.insert(data)
    return str(id)