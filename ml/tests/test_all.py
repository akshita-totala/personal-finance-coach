from ml.services.statement_service import upload_statement
from ml.parser.categorizer import categorize_transaction
from ml.parser.validator import validate_transaction

print("===== Categorizer Test =====")
print(categorize_transaction("SWIGGY"))

print("\n===== Validator Test =====")
transaction = {
    "date": "2026-07-01",
    "description": "SWIGGY",
    "amount": 450.0,
    "type": "Debit"
}
print(validate_transaction(transaction))

print("\n===== Statement Upload Test =====")
print(upload_statement("sample_data/sample.pdf"))

print("\n===== Duplicate Upload Test =====")
print(upload_statement("sample_data/sample.pdf"))

print("\n===== Missing PDF Test =====")
print(upload_statement("sample_data/not_found.pdf"))