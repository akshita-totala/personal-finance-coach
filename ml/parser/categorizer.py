from ml.models.predict_categorizer import predict_category


def categorize_transaction(description, amount):
    """
    Predict transaction category using the trained ML model.
    """

    category, confidence = predict_category(
        description,
        amount
    )

    return category, confidence