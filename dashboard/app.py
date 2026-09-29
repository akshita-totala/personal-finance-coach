import streamlit as st
import psycopg2
import tempfile
import os
import pandas as pd

import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from ml.services.statement_service import upload_statement
from ml.services.db import correct_transaction_category

st.set_page_config(
    page_title="Personal Finance Coach",
    page_icon="💰",
    layout="wide"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1 {
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em;
}

h2, h3 {
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}

[data-testid="stMetricValue"] {
    font-size: 1.7rem;
    font-weight: 600;
}

[data-testid="stMetricLabel"] {
    font-size: 0.9rem;
    font-weight: 500;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Personal Finance Coach")
st.write("Your personal finance dashboard")

# -----------------------------
# Upload Bank Statement
# -----------------------------

st.subheader("📄 Upload Bank Statement")

uploaded_file = st.file_uploader(
    "Upload your bank statement PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Process Statement"):

        temp_path = os.path.join(
            tempfile.gettempdir(),
            uploaded_file.name
        )

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        result = upload_statement(temp_path)

        if result["status"] == "success":
            st.success(
                f"Statement processed successfully! "
                f"{result['transactions_uploaded']} transaction(s) uploaded."
            )

            st.rerun()

        else:
            st.error(result["message"])

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="finance_coach",
        user="postgres",
        password="root"
    )


try:
    conn = connect_db()

    query = """
    SELECT
        id,
        date,
        description,
        amount,
        type,
        category,
        confidence
    FROM transactions
    ORDER BY date DESC;
    """

    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

        # -----------------------------
    # Category Totals
    # -----------------------------

    category_totals = {}

    for row in rows:
        if str(row[4]).lower() == "debit":
            category = row[5]

            if category:
                category_totals[category] = (
                    category_totals.get(category, 0) + float(row[3])
                )

    # -----------------------------
    # Spending Summary
    # -----------------------------

    st.subheader("Spending Summary")

    total_spending = sum(
        row[3]
        for row in rows
        if str(row[4]).lower() == "debit"
    )

    food_spending = sum(
        row[3]
        for row in rows
        if str(row[4]).lower() == "debit"
        and row[5] == "Food"
    )

    transport_spending = sum(
        row[3]
        for row in rows
        if str(row[4]).lower() == "debit"
        and row[5] == "Transport"
    )

    shopping_spending = sum(
        row[3]
        for row in rows
        if str(row[4]).lower() == "debit"
        and row[5] == "Shopping"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Spending",
        f"₹{total_spending:,.2f}"
    )

    col2.metric(
        "🍔 Food",
        f"₹{food_spending:,.2f}"
    )

    col3.metric(
        "🚕 Transport",
        f"₹{transport_spending:,.2f}"
    )

    col4.metric(
        "🛍️ Shopping",
        f"₹{shopping_spending:,.2f}"
    )

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "🏠 Rent",
        f"₹{category_totals.get('Rent', 0):,.2f}"
    )

    col6.metric(
        "🎬 Entertainment",
        f"₹{category_totals.get('Entertainment', 0):,.2f}"
    )

    col7.metric(
        "💡 Utilities",
        f"₹{category_totals.get('Utilities', 0):,.2f}"
    )

    col8.metric(
        "🏥 Healthcare",
        f"₹{category_totals.get('Healthcare', 0):,.2f}"
    )

    # -----------------------------
    # Spending by Category
    # -----------------------------

    

    

    if category_totals:
        st.subheader("Spending by Category")

        st.bar_chart(category_totals)

    st.subheader("Transactions")

    if rows:

        transaction_data = []

        for row in rows:
            transaction_data.append({
                "Date": row[1],
                "Description": row[2],
                "Amount": f"₹{float(row[3]):,.2f}",
                "Type": row[4],
                "Category": row[5],
                "Confidence": (
                    f"{float(row[6]) * 100:.0f}%"
                    if row[6] is not None
                    else "—"
                )
            })

        transaction_df = pd.DataFrame(transaction_data)

        st.dataframe(
            transaction_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No transactions found.")

except Exception as e:
    st.error(f"Database connection failed: {e}")

    # -----------------------------
# Correct Transaction Category
# -----------------------------

st.subheader("✏️ Correct Transaction Category")

transaction_ids = [row[0] for row in rows]

if transaction_ids:

    selected_id = st.selectbox(
        "Select Transaction",
        transaction_ids
    )

    selected_row = next(
        row for row in rows
        if row[0] == selected_id
    )

    st.write(
        f"**{selected_row[2]}** — ₹{float(selected_row[3]):,.2f}"
    )

    categories = [
        "Food",
        "Rent",
        "Transport",
        "Entertainment",
        "Utilities",
        "Healthcare",
        "Shopping",
        "Others"
    ]

    current_category = selected_row[5]

    selected_category = st.selectbox(
        "Correct Category",
        categories,
        index=(
            categories.index(current_category)
            if current_category in categories
            else 0
        )
    )

    if st.button("Save Correction"):

        if selected_category == current_category:
            st.info("The transaction already has this category.")

        else:
            correct_transaction_category(
                transaction_id=selected_id,
                corrected_category=selected_category
            )

            st.success(
                f"Transaction {selected_id} updated to "
                f"{selected_category}."
            )

            st.rerun()