import csv
import matplotlib.pyplot as plt
import numpy as np

# Lettura dei dati dai file CSV
csv_files = ['execution_times_mongo.csv', 'execution_times_neo4j.csv']
databases = ['MongoDB', 'Neo4j']  # Nomi dei database

query_execution_times = {}  # Dizionario per memorizzare i tempi di esecuzione delle query
sizes = []  # Lista per memorizzare le dimensioni dei database

for csv_file in csv_files:
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            query = row['Query']
            size = row['Dimensione']
            execution_time = float(row['Tempo di esecuzione medio (ms)'])
            
            if query not in query_execution_times:
                query_execution_times[query] = {}
            query_execution_times[query][size] = {csv_file: execution_time}
            if size not in sizes:
                sizes.append(size)

# Creazione dei grafici a istogramma separati per ogni query e database
colors = plt.cm.get_cmap('tab10', len(sizes))
bar_width = 0.2  # Larghezza delle colonne
x_positions = np.arange(len(sizes))

for query_idx, query_label in enumerate(query_execution_times.keys()):
    plt.figure(figsize=(12, 6))
    plt.title(f'Tempi di esecuzione per la query: {query_label}')
    plt.xlabel('Dimensione del DB')
    plt.ylabel('Tempo di esecuzione medio (ms)')
    plt.grid(True)

    for db_idx, database in enumerate(databases):
        execution_times = [query_execution_times[query_label][size].get(database, 0) for size in sizes]
        plt.bar(x_positions + (db_idx * bar_width), execution_times, bar_width, color=colors(db_idx), label=database)

    plt.xticks(x_positions + bar_width * ((len(databases) - 1) / 2), sizes)
    plt.legend()
    plt.show()
