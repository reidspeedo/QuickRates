import pandas as pd
import pymongo
import os

connection_string = os.environ.get("MONGO_DB_CONN_STR")
client = pymongo.MongoClient(connection_string)
db = client.quickrate


def add_zipcode(row):
    data = {
        'zip': row[1][0],
        'premium': row[1][1],
        'state': row[1][2]
    }
    id = db.zipcodes.insert(data)
    return id



if __name__ == '__main__':
    state_zips = pd.read_csv(r'/Users/reidrelatores/PycharmProjects/QuickRate/nerdwallet_scraper/zip_avg_premium.csv')
    results = [add_zipcode(row) for row in state_zips.iterrows()]
    print(results)