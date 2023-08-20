from pymongo import MongoClient
import time
import csv

sizes = [0.25, 0.50, 0.75, 1.00]

queries = [
    {"collection": "clients", "pipeline": [{"$match": {"Client Name": "Timothy Garcia"}}]},
    {"collection": "transactions", "pipeline": [{"$match": {"Transaction Date": {"$gte": "2023-01-01"}}}]},
    {"collection": "merchants", "pipeline": [{"$match": {"Category": "Retail"}}]},
    {"collection": "suspicious_transactions", "pipeline": [{"$match": {"Amount": {"$gte": 200}}}]},
]

client = MongoClient('mongodb://localhost:27017')

execution_times = []

for size in sizes:
    print(f"Dimension: {int(size * 100)}%")
    
    db_name = f"Fraud{int(size * 100)}"
    db = client[db_name]
    
    for query_idx, query_data in enumerate(queries):
        collection_name = query_data.get("collection", None)
        collection_name = collection_name + "_" + str(int(size * 100))
        
        pipeline = query_data.get("pipeline", None)
        first_execution_time = None
        avg_execution_time = 0

        for _ in range(30):
            start_time = time.time()
            
            result = list(db[collection_name].aggregate(pipeline))
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            avg_execution_time += execution_time
            
            if first_execution_time is None:
                first_execution_time = execution_time
        
        avg_execution_time /= 30
        
        execution_times.append({
            "Query": f"Query {query_idx + 1}",
            "Dimensione": f'{int(size * 100)}%',
            "Tempo di esecuzione medio (ms)": avg_execution_time,
            "Tempo della prima esecuzione (ms)": first_execution_time
        })

    print("-" * 40)

csv_file = 'execution_times_mongo.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Query', 'Dimensione', 'Tempo di esecuzione medio (ms)', 'Tempo della prima esecuzione (ms)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data in execution_times:
        writer.writerow(data)
