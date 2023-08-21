from pymongo import MongoClient
import time
import csv

sizes = [0.25, 0.50, 0.75, 1.00]

queries = [
    {
        "steps": [
            {
                "collection": "clients",
                "pipeline": [
                    {"$match": {"Client Name": "Stephen Cortez"}}
                ]
            }
        ]
    },
    {
        "steps": [
            {
                "collection": "clients",
                "pipeline": [
                    {"$match": {"Client Name": "Stephen Cortez"}}
                ]
            },
            {
                "collection": "transactions",
                "pipeline": [
                    {
                        "$lookup": {
                            "from": "clients",
                            "localField": "Client ID",
                            "foreignField": "Client ID",
                            "as": "client"
                        }
                    },
                    {
                        "$unwind": "$client"
                    },
                    {
                        "$match": {"client.Client Name": "Stephen Cortez"}
                    }
                ]
            }
        ]
    },
    {
        "steps": [
            {
                "collection": "clients",
                "pipeline": [
                    {"$match": {"Client Name": "Stephen Cortez"}}
                ]
            },
            {
                "collection": "transactions",
                "pipeline": [
                    {
                        "$lookup": {
                            "from": "clients",
                            "localField": "Client ID",
                            "foreignField": "Client ID",
                            "as": "client"
                        }
                    },
                    {
                        "$unwind": "$client"
                    },
                    {
                        "$match": {"client.Client Name": "Stephen Cortez"}
                    }
                ]
            },
            {
                "collection": "suspicious_transactions",
                "pipeline": [
                    {"$match": {"Client ID": "$$client.Client ID"}}
                ]
            }
        ]
    },
    {
        "steps": [
            {
                "collection": "clients",
                "pipeline": [
                    {"$match": {"Client Name": "Stephen Cortez"}}
                ]
            },
            {
                "collection": "transactions",
                "pipeline": [
                    {
                        "$lookup": {
                            "from": "clients",
                            "localField": "Client ID",
                            "foreignField": "Client ID",
                            "as": "client"
                        }
                    },
                    {
                        "$unwind": "$client"
                    },
                    {
                        "$match": {"client.Client Name": "Stephen Cortez"}
                    }
                ]
            },
            {
                "collection": "suspicious_transactions",
                "pipeline": [
                    {"$match": {"Client ID": "$$client.Client ID"}}
                ]
            },
            {
                "collection": "fraud_alerts",
                "pipeline": [
                    {"$match": {"Suspicious Transaction ID": "$$CURRENT.Transaction ID"}}
                ]
            }
        ]
    }
]



client = MongoClient('mongodb://localhost:27017')

execution_times = []

for size in sizes:
    print(f"Dimension: {int(size * 100)}%")
    
    db_name = f"Fraud{int(size * 100)}"
    db = client[db_name]
    
    for query_idx, query_data in enumerate(queries):
        steps = query_data.get("steps", [])
        print(f"Query {query_idx + 1} - Steps: {len(steps)}")
        
        first_execution_time = None
        avg_execution_time = 0
        
        for _ in range(30):
            start_time = time.time()
            
            for step in steps:
                collection_name = step.get("collection", None)
                collection_name = collection_name + "_" + str(int(size * 100))
                pipeline = step.get("pipeline", None)
                
                result = list(db[collection_name].aggregate(pipeline))
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            avg_execution_time += execution_time
            
            if first_execution_time is None:
                first_execution_time = execution_time
        
        avg_execution_time /= 30
        print(result)
        
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





