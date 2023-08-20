from faker import Faker
import random
import csv
import uuid
import os

fake = Faker()

def generate_clients(num_records):
    return [
        {"Client Name": fake.name(), "Phone number": fake.phone_number(), "Address": fake.address(), "Email": fake.email()}
        for _ in range(num_records*2)
    ]

def generate_transactions(num_records):
    return [
        {"Client ID": str(uuid.uuid4()), "Transaction Date": fake.date_time_this_year(), "Amount": random.uniform(10, 500), "Description": fake.sentence()}
        for _ in range(num_records*3)
    ]

def generate_merchants(num_records):
    return [
        {"Merchant Name": fake.company(), "Category": fake.random_element(["Retail", "Restaurant", "Online", "Entertainment"]), "Location": fake.city()}
        for _ in range(num_records*1)
    ]

def generate_suspicious_transactions(num_records):
    return [
        {"Transaction ID": str(uuid.uuid4()), "Client ID": str(uuid.uuid4()), "Transaction Date": fake.date_time_this_year(), "Amount": random.uniform(10, 500), "Reason": fake.sentence()}
        for _ in range(num_records*2)
    ]

def generate_fraud_alerts(num_records):
    return [
        {"Alert ID": str(uuid.uuid4()), "Transaction ID": str(uuid.uuid4()), "Alert Date": fake.date_time_this_year(), "Alert Type": fake.random_element(["Chargeback", "Suspicious Activity"]), "Alert Description": fake.sentence()}
        for _ in range(num_records*1)
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
    "transaction" : generate_transactions,
    "merchants" : generate_merchants,
    "suspicious_transactions" : generate_suspicious_transactions,
    "fraud_alerts": generate_fraud_alerts
}

db_sizes = [0.25, 0.50, 0.75, 1.00]
max_records = 5000


for entity_name, generate_function in entities.items():
    for size in db_sizes:
        num_records = int(size * max_records)
        data = generate_function(num_records)
        
        # Crea il percorso della cartella basato sulla dimensione del DB
        db_folder = f"db_{int(size * 100)}"
        os.makedirs(db_folder, exist_ok=True)  # Crea la cartella se non esiste
        
        file_name = f"{entity_name}_{int(size * 100)}.csv"
        file_path = os.path.join(db_folder, file_name)  # Percorso completo del file
        
        generate_csv(data, file_path)
        
        print(f"Generated records for {entity_name} in {file_path}") 
