import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier


TRAIN_PATH = "ml/data/feedback_training_data.csv"

MODEL_PATH = "ml/models/categorizer_model.pkl"
VECTORIZER_PATH = "ml/models/tfidf_vectorizer.pkl"


train = pd.read_csv(TRAIN_PATH)


vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=1
)

X_text = vectorizer.fit_transform(train["description"])
X_amount = train[["amount"]].values

from scipy.sparse import hstack

X = hstack([X_text, X_amount])

y = train["category"]


model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X, y)


joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("Model saved:", MODEL_PATH)
print("Vectorizer saved:", VECTORIZER_PATH)
print("Training rows:", len(train))
print("Categories:", sorted(y.unique()))