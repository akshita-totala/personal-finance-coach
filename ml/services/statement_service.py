import os

from ml.parser.parser_service import process_pdf
from ml.services.db import (
    statement_exists,
    insert_statement,
    insert_transaction,
    log_event,
)


def upload_statement(pdf_path):
    try:
        transactions = process_pdf(pdf_path)

        filename = os.path.basename(pdf_path)

        if statement_exists(filename):
            log_event(
                action="Duplicate Upload",
                resource=filename
            )

            return {
                "status": "error",
                "message": "Statement already uploaded."
            }

        statement_id = insert_statement(filename)

        for transaction in transactions:
            insert_transaction(transaction, statement_id)

        log_event(
            action="Statement Uploaded",
            resource=filename
        )

        return {
            "status": "success",
            "statement_id": statement_id,
            "transactions_uploaded": len(transactions)
        }

    except Exception as e:
        filename = os.path.basename(pdf_path)

        log_event(
            action="Upload Failed",
            resource=filename
        )

        return {
            "status": "error",
            "message": str(e)
        }