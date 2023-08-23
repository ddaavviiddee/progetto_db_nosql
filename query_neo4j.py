from py2neo import Graph
import time
import csv

sizes = [25, 50, 75, 100]

queries = [
    """
    MATCH (c:clients_{size})
    WHERE c.`Client Name` = 'Stephen Cortez'
    RETURN c
    """,
    """
    MATCH (c:clients_{size})
    WHERE c.`Client Name` = 'Stephen Cortez'
    MATCH (t:transactions_{size})-[:MADE_BY]->(c)
    RETURN t
    """,
    """
    MATCH (c:clients_{size})
    WHERE c.`Client Name` = 'Stephen Cortez'
    MATCH (t:transactions_{size})-[:MADE_BY]->(c)
    MATCH (s:suspicious_transactions_{size})-[:IS_SUSPICIOUS]->(t)
    RETURN s
    """,
    """
    MATCH (c:clients_{size})
    WHERE c.`Client Name` = 'Stephen Cortez'
    MATCH (t:transactions_{size})-[:MADE_BY]->(c)
    MATCH (s:suspicious_transactions_{size})-[:IS_SUSPICIOUS]->(t)
    MATCH (f:fraud_alerts_{size})-[:FRAUD]->(s)
    RETURN f
    """
]

execution_times = []

for size in sizes:
    print(f"Dimension: {size}%")
    
    db_name = f"fraud{size}"
    graph = Graph(f"bolt://localhost:7687/{db_name}", user="neo4j", password="password", name=db_name)
    
    for query_idx, query in enumerate(queries):
        print(f"Query {query_idx + 1}")
        
        first_execution_time = None
        avg_execution_time = 0
        
        for _ in range(30):
            start_time = time.time()
            
            result = graph.run(query.format(size=size)).data()
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            avg_execution_time += execution_time
            
            if first_execution_time is None:
                first_execution_time = execution_time
        
        avg_execution_time /= 30
        print(result)
        
        execution_times.append({
            "Query": f"Query {query_idx + 1}",
            "Dimensione": f'{size}%',
            "Tempo di esecuzione medio (ms)": avg_execution_time,
            "Tempo della prima esecuzione (ms)": first_execution_time
        })

    print("-" * 40)

csv_file = 'execution_times_neo4j.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Query', 'Dimensione', 'Tempo di esecuzione medio (ms)', 'Tempo della prima esecuzione (ms)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data in execution_times:
        writer.writerow(data)
