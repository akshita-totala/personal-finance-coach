import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from scipy.sparse import hstack


train = pd.read_csv("ml/data/india_train.csv")
test = pd.read_csv("ml/data/india_test.csv")


vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=1
)

X_train_text = vectorizer.fit_transform(train["description"])
X_test_text = vectorizer.transform(test["description"])

X_train_amount = train[["amount"]].values
X_test_amount = test[["amount"]].values

X_train = hstack([X_train_text, X_train_amount])
X_test = hstack([X_test_text, X_test_amount])

y_train = train["category"]
y_test = test["category"]


model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

f1 = f1_score(
    y_test,
    predictions,
    average="weighted"
)

print("India-only Weighted F1:", round(f1, 4))

print("\nClassification Report:")
print(classification_report(y_test, predictions))