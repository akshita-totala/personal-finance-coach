
from ml.services.db import connect_db


def fetch_transactions(start_date=None, end_date=None):
    """Fetch transactions from PostgreSQL."""

    conn = connect_db()

    try:
        with conn.cursor() as cur:
            query = """
                SELECT id, date, description, amount,
                       type, category, is_anomaly
                FROM transactions
                WHERE LOWER(type) IN ('debit', 'credit')
            """

            params = []

            if start_date:
                query += " AND date >= %s"
                params.append(start_date)

            if end_date:
                query += " AND date <= %s"
                params.append(end_date)

            query += " ORDER BY date"

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

        return rows

    finally:
        conn.close()


def get_spending_summary(start_date=None, end_date=None):
    """Calculate overall spending and income."""

    transactions = fetch_transactions(start_date, end_date)

    total_spending = 0
    total_income = 0

    for row in transactions:
        amount = float(row[3])
        transaction_type = row[4].lower()

        if transaction_type == "debit":
            total_spending += amount
        elif transaction_type == "credit":
            total_income += amount

    return {
        "total_spending": round(total_spending, 2),
        "total_income": round(total_income, 2),
        "net_cash_flow": round(total_income - total_spending, 2),
        "transaction_count": len(transactions)
    }


def get_category_breakdown(start_date=None, end_date=None):
    """Calculate debit expenditure grouped by category."""

    transactions = fetch_transactions(start_date, end_date)

    category_totals = {}

    for row in transactions:
        transaction_type = row[4].lower()

        if transaction_type != "debit":
            continue

        category = row[5] or "Uncategorized"
        amount = float(row[3])

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    return dict(
        sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )


def get_monthly_spending():
    """Calculate expenditure grouped by month."""

    transactions = fetch_transactions()

    monthly_totals = {}

    for row in transactions:
        transaction_date = row[1]
        transaction_type = row[4].lower()

        if transaction_type != "debit":
            continue

        month = transaction_date.strftime("%Y-%m")
        amount = float(row[3])

        monthly_totals[month] = (
            monthly_totals.get(month, 0) + amount
        )

    return dict(sorted(monthly_totals.items()))
