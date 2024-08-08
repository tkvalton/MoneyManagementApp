import csv
from datetime import datetime

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Unable to parse date: {date_string}")

def import_csv(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        
        for row in csv_reader:
            try:
                date = parse_date(row[0])
                transaction_type = row[1]
                sort_code = row[2]
                account_number = row[3]
                description = row[4]
                amount = float(row[5].replace('£', '').replace(',', ''))
                balance = float(row[6].replace('£', '').replace(',', ''))
                
                data.append([date, transaction_type, sort_code, account_number, description, amount, balance])
            except (ValueError, IndexError) as e:
                print(f"Error processing row: {row}. Error: {e}")
                continue
    return data