from ml.services.db import correct_transaction_category


correct_transaction_category(
    transaction_id=9,
    corrected_category="Entertainment"
)

print("Transaction corrected successfully!")