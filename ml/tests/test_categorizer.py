from ml.parser.categorizer import categorize_transaction

transactions = [
    "SWIGGY",
    "AMAZON",
    "UBER",
    "NETFLIX",
    "SALARY",
    "UNKNOWN STORE"
]

for t in transactions:
    print(f"{t} -> {categorize_transaction(t)}")