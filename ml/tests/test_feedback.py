from ml.services.db import insert_feedback


insert_feedback(
    transaction_id=9,
    original_category="Food",
    corrected_category="Others"
)

print("Feedback inserted successfully!")