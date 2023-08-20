import csv
import matplotlib.pyplot as plt

# Lettura dei dati dal file CSV
csv_file = 'execution_times_mongo.csv'
query_execution_times = {}  # Dizionario per memorizzare i tempi di esecuzione delle query
sizes = []  # Lista per memorizzare le dimensioni dei database
query_labels = []  # Lista per memorizzare le etichette delle query
first_execution_times = {}  # Dizionario per memorizzare i tempi della prima esecuzione delle query

with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        query = row['Query']
        size = int(row['Dimensione'].strip('%'))  # Converti in valore intero
        execution_time = float(row['Tempo di esecuzione medio (ms)'])
        first_execution_time = float(row['Tempo della prima esecuzione (ms)'])
        
        if query not in query_execution_times:
            query_execution_times[query] = []
        query_execution_times[query].append((size, execution_time))
        
        if size not in sizes:
            sizes.append(size)
        if query not in query_labels:
            query_labels.append(query)
        
        first_execution_times[query] = first_execution_time

# Creazione dei grafici a istogramma separati per ogni query
colors = plt.cm.get_cmap('tab10', len(sizes))
for query_label in query_labels:
    plt.figure(figsize=(10, 6))
    plt.title(f'Tempi di esecuzione per la query: {query_label}')
    plt.xlabel('Dimensione del DB')
    plt.ylabel('Tempo di esecuzione medio (ms)')
    plt.grid(True)

    x_positions = list(range(len(sizes)))

    for idx, size in enumerate(sizes):
        data = query_execution_times[query_label]
        execution_time = [d[1] for d in data if d[0] == size][0]
        plt.bar(x_positions[idx], execution_time, color=colors(idx), label=f'{size}%')
        plt.text(x_positions[idx], execution_time, f"{first_execution_times[query_label]:.2f}", ha='center', va='bottom')

    plt.xticks(x_positions, sizes)
    plt.legend()
    plt.show()
