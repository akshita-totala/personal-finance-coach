from ml.parser.pdf_reader import extract_text_from_pdf
from ml.parser.local_parser import parse_transactions
from ml.services.db import insert_transaction

pdf_path = "sample_data/sample.pdf"

text = extract_text_from_pdf(pdf_path)

transactions = parse_transactions(text)

for transaction in transactions:
    insert_transaction(transaction)

print("Transaction inserted successfully!")