from ml.parser.parser_service import process_pdf

transactions = process_pdf("sample_data/sample.pdf")

print("Valid Transactions:")

for transaction in transactions:
    print(transaction)