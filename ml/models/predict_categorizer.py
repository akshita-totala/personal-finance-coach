import joblib
from scipy.sparse import hstack


MODEL_PATH = "ml/models/categorizer_model.pkl"
VECTORIZER_PATH = "ml/models/tfidf_vectorizer.pkl"


model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_category(description, amount):
    """
    Predict transaction category and confidence.
    """

    text_features = vectorizer.transform([description])
    amount_features = [[amount]]

    X = hstack([text_features, amount_features])

    prediction = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]
    confidence = max(probabilities)

    if confidence < 0.60:
        return "Others", confidence

    return prediction, confidence


if __name__ == "__main__":

    test_transactions = [
        ("SWIGGY ORDER", 450),
        ("UBER RIDE", 250),
        ("NETFLIX SUBSCRIPTION", 649),
        ("AMAZON ORDER", 1500),
        ("ELECTRICITY BILL", 1800)
    ]

    for description, amount in test_transactions:

        category, confidence = predict_category(
            description,
            amount
        )

        print(
            f"{description} → {category} "
            f"(confidence: {confidence:.2f})"
        )