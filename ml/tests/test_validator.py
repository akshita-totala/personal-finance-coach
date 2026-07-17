from ml.parser.validator import validate_transaction

valid_transaction = {
    "date": "2026-07-01",
    "description": "SWIGGY",
    "amount": 450.0,
    "type": "Debit"
}

invalid_transaction = {
    "date": "",
    "description": "",
    "amount": -100,
    "type": ""
}

print("Valid Transaction:")
print(validate_transaction(valid_transaction))

print()

print("Invalid Transaction:")
print(validate_transaction(invalid_transaction))