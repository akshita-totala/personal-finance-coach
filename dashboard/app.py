
import os
import sys
import tempfile

import pandas as pd
import streamlit as st

# Make project root importable
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, PROJECT_ROOT)

from ml.services.db import (
    connect_db,
    correct_transaction_category
)
from ml.services.statement_service import upload_statement

from ml.analytics.spending_analysis import (
    get_spending_summary,
    get_category_breakdown,
    get_monthly_spending
)
from ml.analytics.anomaly_detection import (
    detect_database_anomalies
)
from ml.analytics.forecasting import (
    forecast_from_database
)
from ml.analytics.financial_insights import (
    generate_financial_insights
)


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

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
}

[data-testid="stMetricValue"] {
    font-size: 1.7rem;
    font-weight: 600;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("💰 Personal Finance Coach")
st.write("Your personal finance dashboard")


# -------------------------------------------------
# PDF UPLOAD
# -------------------------------------------------

st.subheader("📄 Upload Bank Statement")

uploaded_file = st.file_uploader(
    "Upload your bank statement PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Process Statement"):

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(uploaded_file.getbuffer())
                temp_path = temp_file.name

            result = upload_statement(temp_path)

            if result["status"] == "success":
                st.success(
                    f"Statement processed successfully! "
                    f"{result['transactions_uploaded']} "
                    "transaction(s) uploaded."
                )
                st.rerun()

            else:
                st.error(result["message"])

        except Exception as error:
            st.error(f"Statement processing failed: {error}")

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)


st.divider()


# -------------------------------------------------
# FETCH TRANSACTIONS
# -------------------------------------------------

rows = []
database_available = False

try:
    conn = connect_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    date,
                    description,
                    amount,
                    type,
                    category,
                    confidence,
                    is_anomaly
                FROM transactions
                ORDER BY date DESC, id DESC;
            """)

            rows = cursor.fetchall()

        database_available = True

    finally:
        conn.close()

except Exception as error:
    st.error(f"Database connection failed: {error}")


# -------------------------------------------------
# DASHBOARD TABS
# -------------------------------------------------

overview_tab, analytics_tab, transactions_tab, corrections_tab = (
    st.tabs([
        "📊 Overview",
        "🧠 Financial Analytics",
        "📋 Transactions",
        "✏️ Corrections"
    ])
)


# =================================================
# TAB 1: OVERVIEW
# =================================================

with overview_tab:

    st.header("Spending Overview")

    if database_available:

        try:
            summary = get_spending_summary()
            categories = get_category_breakdown()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "💰 Total Spending",
                f"₹{summary['total_spending']:,.2f}"
            )

            col2.metric(
                "💵 Total Income",
                f"₹{summary['total_income']:,.2f}"
            )

            col3.metric(
                "📈 Net Cash Flow",
                f"₹{summary['net_cash_flow']:,.2f}"
            )

            col4.metric(
                "🧾 Transactions",
                summary["transaction_count"]
            )

            st.subheader("Category-wise Spending")

            if categories:

                category_df = pd.DataFrame(
                    list(categories.items()),
                    columns=["Category", "Amount"]
                )

                st.bar_chart(
                    category_df.set_index("Category")
                )

            else:
                st.info("No debit transactions available.")

            st.subheader("Category Summary")

            if categories:
                st.dataframe(
                    category_df,
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as error:
            st.error(f"Unable to load spending overview: {error}")

    else:
        st.warning("Database is currently unavailable.")


# =================================================
# TAB 2: FINANCIAL ANALYTICS
# =================================================

with analytics_tab:

    st.header("Financial Intelligence")

    if database_available:

        # -----------------------------------------
        # MONTHLY SPENDING
        # -----------------------------------------

        st.subheader("📅 Monthly Spending Trends")

        try:
            monthly_data = get_monthly_spending()

            if monthly_data:

                monthly_df = pd.DataFrame(
                    list(monthly_data.items()),
                    columns=["Month", "Spending"]
                )

                st.bar_chart(
                    monthly_df.set_index("Month")
                )

                st.dataframe(
                    monthly_df,
                    use_container_width=True,
                    hide_index=True
                )

                if len(monthly_data) < 2:
                    st.info(
                        "Upload statements covering additional "
                        "months to enable month-over-month comparisons."
                    )

            else:
                st.info("No monthly spending data available.")

        except Exception as error:
            st.error(f"Monthly analysis failed: {error}")

        st.divider()

        # -----------------------------------------
        # ANOMALY DETECTION
        # -----------------------------------------

        st.subheader("🚨 Unusual Transaction Detection")

        try:
            anomalies = detect_database_anomalies()

            if anomalies:

                st.warning(
                    f"{len(anomalies)} potential unusual "
                    "transaction(s) detected."
                )

                anomaly_df = pd.DataFrame(anomalies)

                st.dataframe(
                    anomaly_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.caption(
                    "These are statistical flags, not confirmed fraud."
                )

            else:
                st.success(
                    "No potential unusual transactions detected "
                    "with the current data and detection threshold."
                )

                st.caption(
                    "Categories with insufficient observations "
                    "are excluded from detection."
                )

        except Exception as error:
            st.error(f"Anomaly detection failed: {error}")

        # Show previously persisted flags separately
        persisted_anomalies = [
            row for row in rows if row[7] is True
        ]

        st.caption(
            f"Previously stored anomaly flags: "
            f"{len(persisted_anomalies)}"
        )

        st.divider()

        # -----------------------------------------
        # EXPENSE FORECASTING
        # -----------------------------------------

        st.subheader("🔮 Monthly Expense Forecast")

        try:
            forecast = forecast_from_database(periods=1)

            st.metric(
                "Moving Average Baseline",
                f"₹{forecast['moving_average_baseline']:,.2f}"
            )

            forecast_df = pd.DataFrame(
                forecast["forecasts"]
            )

            st.dataframe(
                forecast_df,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Forecasts are estimates based on historical "
                "monthly expenditure, not guaranteed outcomes."
            )

        except ValueError as error:
            st.info(
                f"Forecast currently unavailable: {error}"
            )

        except Exception as error:
            st.error(f"Forecasting failed: {error}")

        st.divider()

        # -----------------------------------------
        # FINANCIAL INSIGHTS
        # -----------------------------------------

        st.subheader("💡 Personal Financial Insights")

        try:
            insights = generate_financial_insights()

            for index, insight in enumerate(insights, start=1):
                st.write(f"**{index}.** {insight}")

        except Exception as error:
            st.error(f"Unable to generate insights: {error}")

    else:
        st.warning(
            "Connect to the database to view financial analytics."
        )


# =================================================
# TAB 3: TRANSACTIONS
# =================================================

with transactions_tab:

    st.header("Transaction History")

    if database_available and rows:

        transaction_data = []

        for row in rows:
            transaction_data.append({
                "ID": row[0],
                "Date": row[1],
                "Description": row[2],
                "Amount": f"₹{float(row[3]):,.2f}",
                "Type": row[4],
                "Category": row[5],
                "Confidence": (
                    f"{float(row[6]) * 100:.0f}%"
                    if row[6] is not None
                    else "—"
                ),
                "Potential Anomaly": (
                    "Yes" if row[7] else "No"
                )
            })

        transaction_df = pd.DataFrame(transaction_data)

        st.dataframe(
            transaction_df,
            use_container_width=True,
            hide_index=True
        )

    elif database_available:
        st.info("No transactions found.")

    else:
        st.warning("Database is unavailable.")


# =================================================
# TAB 4: MANUAL CATEGORY CORRECTIONS
# =================================================

with corrections_tab:

    st.header("✏️ Correct Transaction Category")

    if database_available and rows:

        transaction_ids = [row[0] for row in rows]

        selected_id = st.selectbox(
            "Select Transaction",
            transaction_ids
        )

        selected_row = next(
            row for row in rows
            if row[0] == selected_id
        )

        st.write(
            f"**{selected_row[2]}** — "
            f"₹{float(selected_row[3]):,.2f}"
        )

        st.write(
            f"Current category: **{selected_row[5]}**"
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

                st.info(
                    "The transaction already has this category."
                )

            else:

                try:
                    correct_transaction_category(
                        transaction_id=selected_id,
                        corrected_category=selected_category
                    )

                    st.success(
                        f"Transaction {selected_id} updated to "
                        f"{selected_category}."
                    )

                    st.rerun()

                except Exception as error:
                    st.error(
                        f"Unable to save correction: {error}"
                    )

    elif database_available:
        st.info("No transactions available for correction.")

    else:
        st.warning("Database is unavailable.")
