from faker import Faker
import random
import csv
import uuid

fake = Faker()

def generate_clients(num_records):
    return [
        {"Client Name": fake.name(), "Phone number": fake.phone_number(), "Address": fake.address(), "Email": fake.email()}
        for _ in range(num_records)
    ]

def generate_transactions(num_records):
    return [
        {"Client ID": str(uuid.uuid4()), "Transaction Date": fake.date_time_this_year(), "Amount": random.uniform(10, 500), "Description": fake.sentence()}
        for _ in range(num_records)
    ]

def generate_merchants(num_records):
    return [
        {"Merchant Name": fake.company(), "Category": fake.random_element(["Retail", "Restaurant", "Online", "Entertainment"]), "Location": fake.city()}
        for _ in range(num_records)
    ]

def generate_suspicious_transactions(num_records):
    return [
        {"Transaction ID": str(uuid.uuid4()), "Client ID": str(uuid.uuid4()), "Transaction Date": fake.date_time_this_year(), "Amount": random.uniform(10, 500), "Reason": fake.sentence()}
        for _ in range(num_records)
    ]

def generate_fraud_alerts(num_records):
    return [
        {"Alert ID": str(uuid.uuid4()), "Transaction ID": str(uuid.uuid4()), "Alert Date": fake.date_time_this_year(), "Alert Type": fake.random_element(["Chargeback", "Suspicious Activity"]), "Alert Description": fake.sentence()}
        for _ in range(num_records)
    ]

def generate_csv(data, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

entities = {
    "clients": generate_clients,
    "transaction" : generate_transactions,
    "merchants" : generate_merchants,
    "suspicious_transactions" : generate_suspicious_transactions,
    "fraud_alerts": generate_fraud_alerts
}

sizes = [0.25, 0.50, 0.75, 1.00]
max_records = 1000


def generate_and_save_data(entity, generate_function):
    for size in sizes:
        num_records = int(size*max_records)
        data = generate_function(num_records)
        file_name = f"{entity}_{int(size*100)}.csv"
        generate_csv(data, file_name)

for entity_name, generate_function in entities.items():
    generate_and_save_data(entity_name, generate_function)
