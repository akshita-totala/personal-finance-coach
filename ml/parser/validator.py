from datetime import datetime


def validate_transaction(transaction):
    """
    Validates a single transaction.
    Returns (True, "") if valid.
    Otherwise returns (False, error_message).
    """

    # Check required fields
    required = ["date", "description", "amount", "type"]

    for field in required:
        if field not in transaction:
            return False, f"Missing field: {field}"

    # Description cannot be empty
    if not transaction["description"].strip():
        return False, "Empty description"

    # Amount must be numeric
    if not isinstance(transaction["amount"], (int, float)):
        return False, "Amount must be numeric"

    # Transaction type
    if transaction["type"].lower() not in ["debit", "credit"]:
        return False, "Invalid transaction type"

    # Date format
    try:
        datetime.strptime(transaction["date"], "%d/%m/%Y")
    except ValueError:
        return False, "Invalid date"

    return True, ""