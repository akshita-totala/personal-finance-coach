
from ml.analytics.spending_analysis import (
    get_spending_summary,
    get_category_breakdown,
    fetch_transactions
)


def generate_financial_insights():
    """Generate observations from actual transaction data."""

    summary = get_spending_summary()
    categories = get_category_breakdown()
    transactions = fetch_transactions()

    insights = []

    if not transactions:
        return ["No transactions available for analysis."]

    spending = summary["total_spending"]
    income = summary["total_income"]

    # Highest spending category
    if categories and spending > 0:
        highest_category = max(categories, key=categories.get)
        highest_amount = categories[highest_category]

        percentage = (highest_amount / spending) * 100

        insights.append(
            f"{highest_category} is your highest spending "
            f"category at ₹{highest_amount:,.2f} "
            f"({percentage:.1f}% of total expenditure)."
        )

    # Uncategorized expenditure
    uncategorized = categories.get("Uncategorized", 0)

    if spending > 0:
        uncategorized_percentage = (
            uncategorized / spending
        ) * 100

        if uncategorized > 0:
            insights.append(
                f"₹{uncategorized:,.2f} "
                f"({uncategorized_percentage:.1f}%) "
                "of your expenditure is uncategorized."
            )

    # Average debit transaction
    debit_amounts = [
        float(row[3])
        for row in transactions
        if str(row[4]).lower() == "debit"
    ]

    if debit_amounts:
        average = sum(debit_amounts) / len(debit_amounts)

        insights.append(
            f"Your average debit transaction is ₹{average:,.2f}."
        )

    # Income and expenditure comparison
    if income > spending:
        insights.append(
            f"Your recorded income exceeds expenditure "
            f"by ₹{income - spending:,.2f}."
        )
    elif income < spending:
        insights.append(
            f"Your recorded expenditure exceeds income "
            f"by ₹{spending - income:,.2f}."
        )
    else:
        insights.append(
            "Your recorded income and expenditure are equal."
        )

    # Existing anomaly flags
    anomaly_count = sum(
        1 for row in transactions if row[6] is True
    )

    insights.append(
        f"{anomaly_count} transaction(s) are currently "
        "marked as potential anomalies in the database."
    )

    return insights
