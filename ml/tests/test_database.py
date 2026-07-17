from ml.parser.parser_service import process_pdf
from ml.services.db import insert_transaction

transactions = process_pdf("sample_data/sample.pdf")

for transaction in transactions:
    insert_transaction(transaction)

print(f"{len(transactions)} transaction(s) inserted successfully!")