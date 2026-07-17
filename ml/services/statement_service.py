from ml.parser.parser_service import process_pdf
from ml.services.db import insert_transaction


def upload_statement(pdf_path):
    """
    Uploads a bank statement.

    Steps:
    1. Read PDF
    2. Parse transactions
    3. Validate transactions
    4. Store transactions in database
    """

    transactions = process_pdf(pdf_path)

    for transaction in transactions:
        insert_transaction(transaction)

    return {
        "status": "success",
        "transactions_uploaded": len(transactions)
    }