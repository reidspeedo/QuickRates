import pickle
import os
import pymongo
import time

connection_string = 'mongodb+srv://mainuser:quickrate@cluster0.bbjks.mongodb.net/quickrate?retryWrites=true&w=majority'
# connection_string = os.environ.get("MONGO_DB_CONN_STR")
client = pymongo.MongoClient(connection_string)
db = client.quickrate

def update_lr_model(model):
    pickled_model = pickle.dumps(model)
    model_name = 'linear-regression'
    result = db.models.find_one({'model_name': model_name})
    data = {'model_name': model_name,
            'last_updated_time': time.time(),
            'model': pickled_model}
    if result is None:
        id = db.models.insert(data)
    else:
        id = db.models.update({'model_name': model_name}, data)
    return str(id)


def get_lr_model():
    pickle_obj = db.models.find_one({'model_name': 'linear-regression'})
    return pickle.loads(pickle_obj['model'])