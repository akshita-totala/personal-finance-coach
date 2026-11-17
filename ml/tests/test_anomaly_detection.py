
from ml.analytics.anomaly_detection import detect_anomalies


def test_detects_unusually_high_transaction():

    transactions = [
        (1, None, "Grocery 1", 100, "debit", "Food", False),
        (2, None, "Grocery 2", 110, "debit", "Food", False),
        (3, None, "Grocery 3", 105, "debit", "Food", False),
        (4, None, "Grocery 4", 115, "debit", "Food", False),
        (5, None, "Grocery 5", 120, "debit", "Food", False),
        (6, None, "Large purchase", 1000, "debit", "Food", False)
    ]

    anomalies = detect_anomalies(transactions)

    assert len(anomalies) == 1
    assert anomalies[0]["id"] == 6

    print("PASS: Unusually high transaction detected.")


def test_ignores_small_groups():

    transactions = [
        (1, None, "Food 1", 100, "debit", "Food", False),
        (2, None, "Food 2", 1000, "debit", "Food", False),
        (3, None, "Food 3", 120, "debit", "Food", False)
    ]

    anomalies = detect_anomalies(transactions)

    assert anomalies == []

    print("PASS: Small category groups are skipped.")


def test_ignores_credit_transactions():

    transactions = [
        (1, None, "Income 1", 100, "credit", "Income", False),
        (2, None, "Income 2", 200, "credit", "Income", False),
        (3, None, "Income 3", 300, "credit", "Income", False),
        (4, None, "Income 4", 10000, "credit", "Income", False)
    ]

    anomalies = detect_anomalies(transactions)

    assert anomalies == []

    print("PASS: Credit transactions are ignored.")


if __name__ == "__main__":
    test_detects_unusually_high_transaction()
    test_ignores_small_groups()
    test_ignores_credit_transactions()

    print("\nAll anomaly detection tests passed!")
