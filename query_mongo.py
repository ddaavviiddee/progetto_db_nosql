from pymongo import MongoClient
import time
import csv

# Definizione delle dimensioni del database
sizes = [0.25, 0.50, 0.75, 1.00]

# Definizione delle query crescenti in complessità
queries = [
    {"Client Name": "John Doe"},
    {"Transaction Date": {"$gte": "2023-01-01"}},
    {"Amount": {"$gte": 100}},
    {"Amount": {"$gte": 100}, "Merchant Name": "XYZ Inc"}
]

# Dizionario per memorizzare i tempi di esecuzione
execution_times = {}

client = MongoClient('mongodb://localhost:27017')


# Ciclo attraverso le dimensioni
for size in sizes:
    print(f"Dimension: {int(size * 100)}%")
    
    # Creazione di una sotto-lista per ogni dimensione
    execution_times[int(size * 100)] = []
    
    # Ciclo attraverso le query
    for query_idx, query in enumerate(queries):
        avg_execution_time = 0
        
        # Seleziona il database
        db_name = f"Fraud{int(size * 100)}"
        db = client[db_name]
        
        # Esegui la query e misura il tempo di esecuzione
        for _ in range(3):  # Esegui ogni query 3 volte per ottenere una media
            start_time = time.time()
            
            # Esegui la query
            result = db.collection.find(query)
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Converti in millisecondi
            avg_execution_time += execution_time
        
        avg_execution_time /= 3  # Calcola la media dei tempi di esecuzione
        execution_times[int(size * 100)].append(avg_execution_time)
    
    print("-" * 40)

# Creazione dei grafici
query_labels = [f"Query {i+1}" for i in range(len(queries))]
colors = ['b', 'g', 'r', 'c']  # Lista di colori predefiniti

csv_file = 'execution_times_mongo.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Query', 'Size', 'Execution Time (ms)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for query_idx, query_label in enumerate(query_labels):
        for size_idx, size in enumerate(sizes):
            execution_time = execution_times[int(size * 100)][query_idx]
            writer.writerow({'Query': query_label, 'Size': f'{int(size * 100)}%', 'Execution Time (ms)': execution_time})
            
