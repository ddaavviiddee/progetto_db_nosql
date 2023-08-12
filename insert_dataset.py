import csv
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
db = client['Fraud']


def insert_into_mongo(csv_file, collection_name):
    collection = db[collection_name]
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_to_insert = [row for row in reader]
        collection.insert_many(data_to_insert)

insert_into_mongo('dataset_25_percent.csv', 'Fraudinfo25')
insert_into_mongo('dataset_50_percent.csv', 'Fraudinfo50')
insert_into_mongo('dataset_75_percent.csv', 'Fraudinfo75')
insert_into_mongo('dataset_100_percent.csv', 'Fraudinfo100')
