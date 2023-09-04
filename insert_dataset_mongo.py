import csv
from pymongo import MongoClient
import os

client = MongoClient('mongodb://localhost:27017')

sizes = [25, 50, 75, 100]
entities = ["clients", "fraud_alerts", "merchants", "suspicious_transactions", "transactions"]


for size in sizes:
    
    folder_name = f"db_{size}"

    for entity in entities:
        
        db_name = f"Fraud{size}"
        
        file_name = f"{entity}_{size}.csv"
        csv_path = os.path.join(folder_name, file_name)
        

        mongo_db = client[db_name]

        collection = mongo_db[entity]
        collection.delete_many({})
        
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            print("Data extracted from " + csv_path)
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                collection.insert_one(row)



