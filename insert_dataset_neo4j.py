from py2neo import Graph, Node, Relationship
import csv
import os

# Lista di dimensioni
sizes = [25, 50, 75, 100]

# Lista di entità
entities = ["clients", "merchants", "transactions", "suspicious_transactions", "fraud_alerts"]

# Connessione al database Neo4j
for size in sizes:
    db_name = f"fraud{size}"
    graph = Graph(f"bolt://localhost:7687/{db_name}", user="neo4j", password="password", name=db_name)

    folder_name = f"db_{size}"

    # Creazione e caricamento dei nodi
    for entity in entities:
        file_name = f"{entity}_{size}.csv"
        csv_path = os.path.join(folder_name, file_name)

        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            print(f"Data extracted from {csv_path}")
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                node = Node(entity, **row)
                graph.create(node)

    print(f"Nodes loaded for database {db_name}")

    # Creazione delle relazioni tra le entità
    if "transactions" in entities:
        print("Creating transaction relationships")
        transactions = graph.nodes.match(f"transactions")

        for tx_node in transactions:            # Preleva il singolo nodo
            client_id = tx_node["Client ID"]
            merchant_name = tx_node["Merchant Name"]
            # Controlla se ci sono dei match fra i nodi
            client_node = graph.nodes.match(f"clients", **{"Client ID": client_id}).first()        
            merchant_node = graph.nodes.match(f"merchants", **{"Merchant Name": merchant_name}).first()
            # Se ci sono dei match, crea la relazione
            if client_node is not None and merchant_node is not None:
                rel_client = Relationship(tx_node, "MADE_BY", client_node)
                rel_merchant = Relationship(tx_node, "BOUGHT_FROM", merchant_node)
                graph.create(rel_client)
                graph.create(rel_merchant)

        print(f"Relationships created between transactions, clients, and merchants for database {db_name}")

    if "fraud_alerts" in entities:
        print("Creating fraud relationships")
        fraud_alerts = graph.nodes.match(f"fraud_alerts")

        for alert_node in fraud_alerts:
            suspicious_transaction_id = alert_node["Suspicious Transaction ID"]

            suspicious_transaction_node = graph.nodes.match(f"suspicious_transactions", **{"Suspicious Transaction ID": suspicious_transaction_id}).first()

            if suspicious_transaction_node is not None:
                rel_fraud_alert = Relationship(alert_node, "FRAUD", suspicious_transaction_node)
                graph.create(rel_fraud_alert)

        print(f"Relationships created between fraud_alerts and suspicious_transactions for database {db_name}")

    if "suspicious_transactions" in entities:
        print("Creating suspicious relationships")
        suspicious_transactions = graph.nodes.match(f"suspicious_transactions")

        for suspicious_tx_node in suspicious_transactions:
            transaction_id = suspicious_tx_node["Transaction ID"]

            transaction_node = graph.nodes.match(f"transactions", **{"Transaction ID": transaction_id}).first()

            if transaction_node is not None:
                rel_suspicious_tx = Relationship(suspicious_tx_node, "IS_SUSPICIOUS", transaction_node)
                graph.create(rel_suspicious_tx)

        print(f"Relationships created between suspicious_transactions and transactions for database {db_name}")

print("Relationship creation completed.")


