from pymongo import MongoClient
import time
import csv
import numpy as np

sizes = [0.25, 0.50, 0.75, 1.00]

confidence_level = 0.95

execution_times = []

queries = [
    {
    "collection": "clients",
    "pipeline": [
        {
            "$match": {
                "Client Name": "Teresa Padilla"
            }
        }
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
            "$match": {
                "client.Client Name": "Teresa Padilla"
            }
        }
    ]
    },
    {
    "collection": "clients",
    "pipeline": [
        {
            "$match": {
                "Client Name": "Teresa Padilla"
            }
        },
        {
            "$lookup": {
                "from": "transactions",
                "localField": "Client ID",
                "foreignField": "Client ID",
                "as": "client_transactions"
            }
        },
        {
            "$lookup": {
                "from": "suspicious_transactions",
                "localField": "Client ID",
                "foreignField": "Client ID",
                "as": "suspicious_transactions"
            }
        }
    ]
    },
    {
    "collection": "clients",
    "pipeline": [
        {
            "$match": {
                "Client Name": "Teresa Padilla"
            }
        },
        {
            "$lookup": {
                "from": "transactions",
                "localField": "Client ID",
                "foreignField": "Client ID",
                "as": "client_transactions"
            }
        },
        {
            "$lookup": {
                "from": "suspicious_transactions",
                "localField": "Client ID",
                "foreignField": "Client ID",
                "as": "suspicious_transactions"
            }
        },
        {
            "$lookup": {
                "from": "fraud_alerts",
                "localField": "suspicious_transactions.Suspicious Transaction ID",
                "foreignField": "Suspicious Transaction ID",
                "as": "fraud_alerts"
            }
        },
        {
            "$match": {
                "fraud_alerts": { "$exists": "true" }
            }
        }
    ]
}

]



client = MongoClient('mongodb://localhost:27017')

execution_times_for_query = []

for size in sizes:
    print(f"Dimension: {int(size * 100)}%")

    db_name = f"Fraud{int(size * 100)}"
    db = client[db_name]

    for query_idx, query_data in enumerate(queries):
        print(f"Query {query_idx + 1} ")

        collection_name = query_data["collection"]
        pipeline = query_data["pipeline"]

        execution_times_for_query = []  # Lista per memorizzare i tempi di esecuzione

        start_first_execution = time.time()
        first_execution = db[collection_name].aggregate(pipeline)
        end_first_execution = time.time()

        first_execution_time = (end_first_execution - start_first_execution) * 1000 
        
        for _ in range(30):

            start_time = time.time()
            result = list(db[collection_name].aggregate(pipeline))

            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            execution_times_for_query.append(execution_time)

        # Calcola l'intervallo di confidenza
        n = len(execution_times_for_query)
        mean_execution_time = np.mean(execution_times_for_query)
        std_deviation = np.std(execution_times_for_query, ddof=1)
        margin_of_error = std_deviation / np.sqrt(n) * 1.96  # Utilizza 1.96 per il 95% di confidenza

        lower_bound = mean_execution_time - margin_of_error
        upper_bound = mean_execution_time + margin_of_error

        execution_times.append({
            "Query": f"Query {query_idx + 1}",
            "Dimensione": f'{int(size * 100)}%',
            "Tempo della prima esecuzione (ms)": first_execution_time,
            "Tempo di esecuzione medio (ms)": mean_execution_time,
            "Intervallo di confidenza inferiore (ms)": lower_bound,
            "Intervallo di confidenza superiore (ms)": upper_bound
        })

        print(result)


    print("-" * 40)

# Scrivi gli intervalli di confidenza nel file CSV
csv_file = 'execution_times_mongo.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Query', 'Dimensione', 'Tempo della prima esecuzione (ms)', 'Tempo di esecuzione medio (ms)', 'Intervallo di confidenza inferiore (ms)', 'Intervallo di confidenza superiore (ms)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data in execution_times:
        writer.writerow(data)





