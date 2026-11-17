
import numpy as np

from ml.services.db import connect_db


MIN_TRANSACTIONS = 4
IQR_MULTIPLIER = 1.5


def detect_anomalies(transactions, min_transactions=MIN_TRANSACTIONS):
    """
    Detect unusually high debit transactions using IQR.

    Expected transaction format:
    (id, date, description, amount, type, category, is_anomaly)

    Returns a list of detected anomaly details.
    """

    category_groups = {}

    for transaction in transactions:
        transaction_id, date, description, amount, transaction_type, category, _ = transaction

        if str(transaction_type).lower() != "debit":
            continue

        category = category or "Uncategorized"

        category_groups.setdefault(category, []).append({
            "id": transaction_id,
            "date": date,
            "description": description,
            "amount": float(amount),
            "category": category
        })

    anomalies = []

    for category, records in category_groups.items():

        # Insufficient observations for reliable IQR analysis
        if len(records) < min_transactions:
            continue

        amounts = np.array(
            [record["amount"] for record in records],
            dtype=float
        )

        q1 = np.percentile(amounts, 25)
        q3 = np.percentile(amounts, 75)

        iqr = q3 - q1
        upper_limit = q3 + (IQR_MULTIPLIER * iqr)

        for record in records:
            if record["amount"] > upper_limit:
                anomalies.append({
                    **record,
                    "upper_limit": round(float(upper_limit), 2),
                    "reason": "Amount exceeds the category's IQR upper limit"
                })

    return anomalies


def fetch_anomaly_transactions():
    """Fetch debit transactions from PostgreSQL."""

    conn = connect_db()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, date, description, amount,
                       type, category, is_anomaly
                FROM transactions
                WHERE LOWER(type) = 'debit'
                ORDER BY date, id;
            """)

            return cur.fetchall()

    finally:
        conn.close()


def detect_database_anomalies():
    """Run anomaly detection against actual database transactions."""

    transactions = fetch_anomaly_transactions()

    return detect_anomalies(transactions)
