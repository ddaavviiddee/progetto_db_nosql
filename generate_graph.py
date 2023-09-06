import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# Carica i dati dai file CSV
data_mongo = pd.read_csv('execution_times_mongo.csv')
data_neo4j = pd.read_csv('execution_times_neo4j.csv')

# Lista delle dimensioni del dataset
dataset_sizes = ['25%', '50%', '75%', '100%']

# Lista delle query
queries = ['Query 1', 'Query 2', 'Query 3', 'Query 4']

# Definisci i colori per MongoDB e Neo4j
color_mongo = 'seagreen'
color_neo4j = 'slateblue'

green = mpatches.Patch(color='seagreen', label='MongoDB')
blue = mpatches.Patch(color='slateblue', label='Neo4J')

# Per ogni query, crea gli istogrammi
for query in queries:
    # Filtra i dati per la query corrente
    data_mongo_query = data_mongo[data_mongo['Query'] == query]
    data_neo4j_query = data_neo4j[data_neo4j['Query'] == query]
    
    # Crea il primo istogramma con i tempi della prima esecuzione
    plt.figure(figsize=(10, 6))
    for size in dataset_sizes:
        values_mongo = data_mongo_query[data_mongo_query['Dimensione'] == size]['Tempo della prima esecuzione (ms)']
        values_neo4j = data_neo4j_query[data_neo4j_query['Dimensione'] == size]['Tempo della prima esecuzione (ms)']

        bar_values = [values_mongo.values[0], values_neo4j.values[0]]

        plt.bar([f"{size} (MongoDB)", f"{size} (Neo4j)"], bar_values, color=[color_mongo, color_neo4j])
        
    plt.xlabel('Dimensione del Dataset')
    plt.ylabel('Tempo di esecuzione (ms)')
    plt.title(f'Istogramma - Tempo della Prima Esecuzione per {query}')
    plt.tight_layout()
    plt.grid(axis='y', color='grey', linestyle="-.")
    plt.legend(handles=[green,blue])
    plt.show()

    # Crea il secondo istogramma con le medie dei tempi
    plt.figure(figsize=(10, 6))
    for size in dataset_sizes:
        values_mongo = data_mongo_query[data_mongo_query['Dimensione'] == size]['Tempo di esecuzione medio (ms)']
        values_neo4j = data_neo4j_query[data_neo4j_query['Dimensione'] == size]['Tempo di esecuzione medio (ms)']
        
        # Estrai valori minimi e massimi dagli intervalli di confidenza
        conf_mongo_min = data_mongo_query[data_mongo_query['Dimensione'] == size]['Intervallo di confidenza inferiore (ms)']
        conf_mongo_max = data_mongo_query[data_mongo_query['Dimensione'] == size]['Intervallo di confidenza superiore (ms)']
        conf_neo4j_min = data_neo4j_query[data_neo4j_query['Dimensione'] == size]['Intervallo di confidenza inferiore (ms)']
        conf_neo4j_max = data_neo4j_query[data_neo4j_query['Dimensione'] == size]['Intervallo di confidenza superiore (ms)']

        bar_values = [values_mongo.values[0], values_neo4j.values[0]]



        error_mongo = [values_mongo.values[0] - conf_mongo_min.values[0], conf_mongo_max.values[0] - values_mongo.values[0]]
        error_neo4j = [values_neo4j.values[0] - conf_neo4j_min.values[0], conf_neo4j_max.values[0] - values_neo4j.values[0]]


        # Crea gli istogrammi con intervalli di confidenza
        plt.bar([f"{size} (MongoDB)", f"{size} (Neo4j)"], bar_values, color=[color_mongo, color_neo4j], yerr=[error_mongo, error_neo4j], capsize=5)


          
    plt.xlabel('Dimensione del Dataset')
    plt.ylabel('Tempo di esecuzione medio (ms)')
    plt.title(f'Istogramma - Tempo di Esecuzione Medio per {query}')
    plt.tight_layout()
    plt.grid(axis='y', color='grey', linestyle="-.")
    plt.legend(handles=[green,blue])
    plt.show()