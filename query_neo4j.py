from py2neo import Graph
import time
import csv
import numpy as np

sizes = [25, 50, 75, 100]

confidence_level = 0.95

confidence_intervals = []

queries = [
    """
    MATCH (c:clients)
    WHERE c.`Client Name` = 'Teresa Padilla'
    RETURN c
    MATCH (c:clients)
    RETURN count(c) AS ClientCount
    """,
    """
    MATCH (c:clients)
    WHERE c.`Client Name` = 'Teresa Padilla'
    MATCH (t:transactions)-[:MADE_BY]->(c)
    RETURN t
    MATCH (c:clients {`Client Name`: "John Olson"})
    RETURN c
    """,
    """
    MATCH (c:clients)
    WHERE c.`Client Name` = 'Teresa Padilla'
    MATCH (t:transactions)-[:MADE_BY]->(c)
    MATCH (s:suspicious_transactions)-[:IS_SUSPICIOUS]->(t)
    MATCH (c:clients {`Client Name`: "John Olson"})-[:MADE_BY]->(t:transactions)<-[:IS_SUSPICIOUS]-(s:suspicious_transactions)
    RETURN s
    """,
    """
    MATCH (c:clients)
    WHERE c.`Client Name` = 'Teresa Padilla'
    MATCH (t:transactions)-[:MADE_BY]->(c)
    MATCH (s:suspicious_transactions)-[:IS_SUSPICIOUS]->(t)
    MATCH (f:fraud_alerts)-[:FRAUD]->(s)
    RETURN f
    MATCH (c:clients {`Client Name`: "John Olson"})-[:MADE_BY]->(t:transactions)<-[:IS_SUSPICIOUS]-(s:suspicious_transactions)
    WITH s
    MATCH (s)-[:FRAUD]->(f:fraud_alerts)
    RETURN s, f
    """
]

execution_times = []

for size in sizes:
    print(f"Dimension: {size}%")
    
    db_name = f"fraud{size}"
    graph = Graph(f"bolt://localhost:7687/{db_name}", user="neo4j", password="password", name=db_name)
    
    for query_idx, query in enumerate(queries):
        print(f"Query {query_idx + 1}")
        
        execution_times_for_query = []  # Lista per memorizzare i tempi di esecuzione
        start_first_execution = time.time()
        first_exeuction = graph.run(query).data()
        end_first_execution = time.time()

        first_execution_time = (end_first_execution - start_first_execution) * 1000
        for _ in range(30):
            start_time = time.time()
            
            result = graph.run(query).data()
            
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
            "Dimensione": f'{size}%',
            "Tempo della prima esecuzione (ms)": first_execution_time,
            "Tempo di esecuzione medio (ms)": mean_execution_time,
            "Intervallo di confidenza inferiore (ms)": lower_bound,
            "Intervallo di confidenza superiore (ms)": upper_bound
        })
        print(result)

    print("-" * 40)

csv_file = "execution_times_neo4j.csv"

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Query', 'Dimensione', 'Tempo della prima esecuzione (ms)', 'Tempo di esecuzione medio (ms)', 'Intervallo di confidenza inferiore (ms)', 'Intervallo di confidenza superiore (ms)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data in execution_times:
        writer.writerow(data)