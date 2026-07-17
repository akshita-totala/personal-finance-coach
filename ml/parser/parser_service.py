from ml.parser.pdf_reader import extract_text_from_pdf
from ml.parser.local_parser import parse_transactions
from ml.parser.validator import validate_transaction


def process_pdf(pdf_path):
    """
    Complete pipeline:
    PDF -> Text -> Transactions -> Validation
    """

    text = extract_text_from_pdf(pdf_path)
    transactions = parse_transactions(text)

    valid_transactions = []

    for transaction in transactions:
        valid, message = validate_transaction(transaction)

        if valid:
            valid_transactions.append(transaction)
        else:
            print(f"Skipped transaction: {message}")

    return valid_transactions