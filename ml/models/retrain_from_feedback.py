import pandas as pd
from ml.services.db import get_latest_feedback

BASE_TRAIN_PATH = "ml/data/india_train_augmented.csv"
OUTPUT_PATH = "ml/data/feedback_training_data.csv"


def build_feedback_training_data():
    base_train = pd.read_csv(BASE_TRAIN_PATH)

    feedback_rows = get_latest_feedback()

    if not feedback_rows:
        print("No feedback available.")
        return

    feedback_data = pd.DataFrame(
        feedback_rows,
        columns=[
            "transaction_id",
            "description",
            "amount",
            "category"
        ]
    )

    feedback_data = feedback_data[
        ["description", "amount", "category"]
    ]

    combined = pd.concat(
        [base_train, feedback_data],
        ignore_index=True
    )

    combined.to_csv(OUTPUT_PATH, index=False)

    print("Base training rows:", len(base_train))
    print("Feedback rows:", len(feedback_data))
    print("Final training rows:", len(combined))
    print("Saved:", OUTPUT_PATH)


if __name__ == "__main__":
    build_feedback_training_data()