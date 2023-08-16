import csv
import matplotlib.pyplot as plt

# Lettura dei dati dal file CSV
csv_file = 'execution_times_mongo.csv'
query_execution_times = {}  # Dizionario per memorizzare i tempi di esecuzione delle query
sizes = []  # Lista per memorizzare le dimensioni dei database
query_labels = []  # Lista per memorizzare le etichette delle query

with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        query = row['Query']
        size = row['Size']
        execution_time = float(row['Execution Time (ms)'])
        
        if query not in query_execution_times:
            query_execution_times[query] = []
        query_execution_times[query].append((size, execution_time))
        
        if size not in sizes:
            sizes.append(size)
        if query not in query_labels:
            query_labels.append(query)

# Creazione del grafico
colors = plt.cm.get_cmap('tab10', len(query_labels))
plt.figure(figsize=(10, 6))

for query_idx, query_label in enumerate(query_labels):
    data = query_execution_times[query_label]
    sizes_for_query = [d[0] for d in data]
    execution_times_for_query = [d[1] for d in data]
    plt.plot(sizes_for_query, execution_times_for_query, marker='o', label=query_label, color=colors(query_idx))

plt.xlabel('Size of DB')
plt.ylabel('Execution Time (ms)')
plt.title('Query Execution Times by DB Size')
plt.legend()
plt.grid()
plt.show()
