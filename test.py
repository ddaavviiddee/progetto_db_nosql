from faker import Faker
import random
import csv

fake = Faker()

def generate_dataset():
    client_name = fake.name()
    credit_card_numer = fake.credit_card_number(card_type='mastercard')
    transition_date = fake.date_time_this_year(before_now=True, after_now=False)
    transition_import = round(random.uniform(100, 1000), 2)
    description = fake.text()

    return {
        "Client Name": client_name,
        "Credit card number": credit_card_numer,
        "Transition date": transition_date,
        "Transition import": transition_import,
        "Description": description
    }


def generate_and_save(file_name, size):
    
    dataset = [generate_dataset() for _ in range(int(size * 10))]

    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Client Name", "Credit card number", "Transition date", "Transition import", "Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for case in dataset:
            writer.writerow(case)

percentages = [0.25, 0.50, 0.75, 1.0]
max_records = 10000  # Cambia questo valore in base al numero totale di record desiderato

for size in percentages:
    print(size)
    num_record = int(size * max_records)
    file_name = f'dataset_{int(size * 100)}_percent.csv'
    generate_and_save(file_name, num_record)
