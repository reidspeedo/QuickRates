import pickle
import os
import pymongo
import time

connection_string = os.environ.get("MONGO_DB_CONN_STR")
client = pymongo.MongoClient(connection_string)
db = client.quickrate

def update_lr_model(model):
    pickled_model = pickle.dumps(model)
    id = db.models.insert({'model_name': 'linear-regression',
                             'created_time': time.time(),
                             'model': pickled_model})
    return str(id)


def get_lr_model():
    pickle_obj = db.models.find({'model_name': 'linear-regression'})
    out_model = [item for item in pickle_obj][0]
    return pickle.loads(out_model['model'])