from faker import Faker
import random
import csv
import uuid
import os

fake = Faker()

def generate_clients(num_records):
    clients = []
    for _ in range(num_records):
        client = {
            "Client ID": str(uuid.uuid4()),
            "Client Name": fake.name(),
            "Phone number": fake.phone_number(),
            "Address": fake.address(),
            "Email": fake.email()
        }
        clients.append(client)
    return clients

# Genera dati delle transazioni con relazioni ai clienti e commercianti
def generate_transactions(num_records, clients, merchants):
    transactions = []
    for _ in range(num_records):
        client = random.choice(clients)
        merchant = random.choice(merchants)
        
        transaction = {
            "Transaction ID": str(uuid.uuid4()),
            "Client ID": client["Client ID"],
            "Merchant Name": merchant["Merchant Name"],
            "Transaction Date": fake.date_time_this_year(),
            "Amount": random.uniform(10, 500),
            "Description": fake.sentence()
        }
        transactions.append(transaction)
    return transactions

# Genera dati delle transazioni sospette con relazioni ai clienti e transazioni
def generate_suspicious_transactions(num_records, clients, transactions):
    suspicious_transactions = []
    for _ in range(num_records):
        client = random.choice(clients)
        transaction = random.choice(transactions)
        
        suspicious_transaction = {
            "Suspicious Transaction ID": str(uuid.uuid4()),
            "Client ID": client["Client ID"],
            "Transaction ID": transaction["Transaction ID"],
            "Transaction Date": fake.date_time_this_year(),
            "Amount": transaction["Amount"],
            "Reason": fake.sentence()
        }
        suspicious_transactions.append(suspicious_transaction)
    return suspicious_transactions

# Genera dati degli avvisi di frode con relazioni alle transazioni sospette
def generate_fraud_alerts(num_records, suspicious_transactions):
    fraud_alerts = []
    for _ in range(num_records):
        suspicious_transaction = random.choice(suspicious_transactions)
        
        fraud_alert = {
            "Fraud Alert ID": str(uuid.uuid4()),
            "Suspicious Transaction ID": suspicious_transaction["Suspicious Transaction ID"],
            "Alert Date": fake.date_time_this_year(),
            "Alert Type": fake.random_element(["Chargeback", "Suspicious Activity"]),
            "Alert Description": fake.sentence()
        }
        fraud_alerts.append(fraud_alert)
    return fraud_alerts

# Genera dati dei commercianti
def generate_merchants(num_records):
    return [
        {"Merchant Name": fake.company(), "Category": fake.random_element(["Retail", "Restaurant", "Online", "Entertainment"]), "Location": fake.city()}
        for _ in range(num_records)
    ]

def generate_csv(data, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def clear_csv(file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        pass 

entities = {
    "clients": generate_clients,
    "merchants" : generate_merchants,
    "transactions" : generate_transactions,
    "suspicious_transactions" : generate_suspicious_transactions,
    "fraud_alerts": generate_fraud_alerts
}

# ... (codice precedente)

db_sizes = [0.25, 0.50, 0.75, 1.00]
max_records = 10000
clients = generate_clients(max_records)
merchants = generate_merchants(max_records)
transactions = generate_transactions(max_records, clients, merchants)
suspicious_transactions = generate_suspicious_transactions(max_records, clients, transactions)

entity_proportions = {
    "clients": 2,
    "merchants": 1,
    "transactions": 3,
    "suspicious_transactions": 2,
    "fraud_alerts": 1
}

for entity_name, generate_function in entities.items():
    for size in db_sizes:
        max_records_per_entity = int(size * max_records)  # Numero massimo di record per l'entità in base alla dimensione
        
        # Calcola il numero effettivo di record per l'entità proporzionata
        num_records = int(max_records_per_entity * entity_proportions[entity_name])

        if entity_name == "transactions":
            print("generating transactions")
            data = generate_function(num_records, clients, merchants)
        elif entity_name == "suspicious_transactions":
            print("generating sus transactions")
            data = generate_function(num_records, clients, transactions)
        elif entity_name == "fraud_alerts":
            print("generating fraud alerts")
            data = generate_function(num_records, suspicious_transactions)
        else:
            data = generate_function(num_records)
        
        # Crea il percorso della cartella basato sulla dimensione del DB
        db_folder = f"db_{int(size * 100)}"
        os.makedirs(db_folder, exist_ok=True)  # Crea la cartella se non esiste
        
        file_name = f"{entity_name}_{int(size * 100)}.csv"
        file_path = os.path.join(db_folder, file_name)  # Percorso completo del file
        
        generate_csv(data, file_path)
        
        print(f"Generated records for {entity_name} in {file_path}")
