from ml.parser.validator import validate_transaction

transaction = {
    "date": "01/07/2026",
    "description": "SWIGGY",
    "amount": 450.0,
    "type": "Debit"
}

valid, message = validate_transaction(transaction)

print("Valid:", valid)

if message:
    print(message)