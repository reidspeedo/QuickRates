import pymongo
import os

connection_string = 'mongodb+srv://mainuser:quickrate@cluster0.bbjks.mongodb.net/quickrate?retryWrites=true&w=majority'
# connection_string = os.environ.get("MONGO_DB_CONN_STR")
client = pymongo.MongoClient(connection_string)
db = client.quickrate


def get_avg_pre_zip(zip):
    return db.zipcodes.find({'zip': zip})