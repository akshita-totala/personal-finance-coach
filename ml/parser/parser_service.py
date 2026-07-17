from ml.parser.pdf_reader import extract_text_from_pdf
from ml.parser.local_parser import parse_transactions
from ml.parser.validator import validate_transaction
from ml.parser.categorizer import categorize_transaction


def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        raise Exception("PDF contains no readable text.")
    transactions = parse_transactions(text)

    valid_transactions = []

    for transaction in transactions:
        is_valid, message = validate_transaction(transaction)

        if is_valid:
            transaction["category"] = categorize_transaction(
                transaction["description"]
            )

            valid_transactions.append(transaction)

    return valid_transactions