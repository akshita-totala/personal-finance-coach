# Personal Finance Coach

An **ML-driven personal finance system** that extracts, validates, categorizes, and analyzes bank transactions from PDF statements — built as part of a software engineering internship at **Persistent Systems**.

---

## Overview

Most individuals have limited visibility into their spending. Bank statements exist as PDFs, and manually tracking transactions is tedious and error-prone.

The **Personal Finance Coach** automates the process — from PDF ingestion and transaction categorization to financial analytics and insights.

The system combines machine learning, PostgreSQL, and a Streamlit dashboard to help users understand their spending patterns, identify unusual expenses, and explore future spending trends.

---

## Features

| Feature | Status |
|---|---|
| PDF bank statement parsing | ✅ Complete |
| Transaction extraction and structuring | ✅ Complete |
| Data validation (date, amount, type) | ✅ Complete |
| Automatic expense categorization | ✅ Complete |
| ML confidence scoring | ✅ Complete |
| Manual category correction | ✅ Complete |
| Feedback storage and feedback-based retraining | ✅ Complete |
| PostgreSQL storage with audit logging | ✅ Complete |
| Duplicate statement detection | ✅ Complete |
| Graceful error handling | ✅ Complete |
| Streamlit dashboard | ✅ Complete |
| Spending summary and category visualization | ✅ Complete |
| End-to-end statement upload pipeline | ✅ Complete |
| Monthly spending analysis | ✅ Complete |
| Category-wise spending breakdown | ✅ Complete |
| IQR-based anomaly detection | ✅ Implemented |
| Expense forecasting using Linear Regression | ✅ Implemented |
| Automated financial insights | ✅ Complete |
| 500-row held-out ML evaluation | ⏳ Pending |
| Genuine/manual labeling requirement | ⏳ Pending |
| Spring Boot REST API | 🔜 Planned — Sprint 4 |

---

## Tech Stack

### Current

- **Python 3.13** — Core application and analytics
- **PostgreSQL 18** — Relational database
- **pdfplumber** — PDF text extraction
- **psycopg2** — PostgreSQL connectivity
- **python-dotenv** — Environment configuration
- **scikit-learn** — ML categorization and Linear Regression forecasting
- **NumPy** — Numerical computations and anomaly detection
- **Pandas** — Data handling and dashboard tables
- **Streamlit** — Interactive dashboard
- **joblib** — Model persistence

### Planned

- Java Spring Boot — REST API layer
- Docker — Containerization
- GitHub Actions — CI/CD

---

## Project Structure

```text
personal-finance-coach/

├── backend/
│   └── # Java Spring Boot API (planned)

├── dashboard/
│   └── app.py

├── database/
│   └── schema.sql

├── ml/
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── spending_analysis.py
│   │   ├── anomaly_detection.py
│   │   ├── forecasting.py
│   │   └── financial_insights.py
│   │
│   ├── models/
│   │   ├── categorizer_model.pkl
│   │   ├── tfidf_vectorizer.pkl
│   │   ├── train_categorizer.py
│   │   ├── predict_categorizer.py
│   │   └── retrain_from_feedback.py
│   │
│   ├── parser/
│   │   ├── local_parser.py
│   │   ├── parser_service.py
│   │   ├── pdf_reader.py
│   │   ├── categorizer.py
│   │   ├── prompts.py
│   │   └── validator.py
│   │
│   ├── services/
│   │   ├── db.py
│   │   └── statement_service.py
│   │
│   ├── tests/
│   │   ├── test_all.py
│   │   ├── test_categorizer.py
│   │   ├── test_correction.py
│   │   ├── test_database.py
│   │   ├── test_feedback.py
│   │   ├── test_gemini.py
│   │   ├── test_local_parser.py
│   │   ├── test_parser_service.py
│   │   ├── test_pdf_reader.py
│   │   ├── test_statement_service.py
│   │   ├── test_validator.py
│   │   ├── test_spending_analysis.py
│   │   ├── test_anomaly_detection.py
│   │   ├── test_forecasting.py
│   │   └── test_financial_insights.py
│   │
│   └── data/
│       ├── india_transactions.csv
│       ├── india_train.csv
│       ├── india_test.csv
│       ├── india_train_augmented.csv
│       ├── combined_transactions.csv
│       ├── processed_transactions.csv
│       └── Personal_Finance_Dataset.csv
│
├── sample_data/
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Database Schema

The PostgreSQL database contains the following tables:

```text
users         — registered users
statements    — uploaded PDF statements
transactions  — extracted and categorized transactions
audit_logs    — data access and modification events
feedback      — user category corrections used for model improvement
```

Full schema: [`database/schema.sql`](database/schema.sql)

**Note:** Ensure `database/schema.sql` contains the actual table creation statements before using it to initialize a fresh database.

---

## Financial Analytics

Sprint 3 introduces a financial analytics layer built on top of the existing transaction database.

### 1. Spending Analysis

The spending analysis module provides:

- Total expenditure
- Total income
- Net cash flow
- Transaction count
- Category-wise expenditure breakdown
- Monthly spending summaries

### 2. Anomaly Detection

The anomaly detection module uses the **Interquartile Range (IQR)** method to identify potentially unusual debit transactions.

- Analyzes transactions category-wise.
- Uses the upper IQR boundary to identify unusually high transaction amounts.
- Skips categories with insufficient transaction history.
- Ignores credit transactions.

The module currently returns potential anomalies for analysis. Detection results are not automatically persisted into the database's `is_anomaly` field.

### 3. Expense Forecasting

The forecasting module uses **Linear Regression** to estimate future monthly expenditure based on historical spending.

- Uses monthly spending data.
- Handles missing months.
- Includes a moving-average baseline.
- Requires at least three consecutive months of historical spending data.

**Current limitation:** The development database currently contains only one month of transaction history. Therefore, a real database-based forecast is unavailable until additional monthly data is added. Forecasting functionality has been tested using controlled sample datasets.

### 4. Financial Insights

The financial insights module generates observations based on available transaction data, including:

- Highest spending category
- Uncategorized expenditure and its percentage of total spending
- Average debit transaction amount
- Income versus expenditure comparison
- Count of transactions currently marked as potential anomalies in the database

### 5. Dashboard Integration

The Streamlit dashboard includes:

- Overview of income, expenditure, and cash flow
- Category-wise spending visualization
- Monthly spending analysis
- Potential anomaly detection results
- Expense forecasting
- Automatically generated financial insights
- Transaction history
- Manual category correction

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/akshita-totala/personal-finance-coach.git
cd personal-finance-coach
```

### 2. Install dependencies

```bash
pip install -r ml/requirements.txt
```

### 3. Set up the database

Create a PostgreSQL database named `finance_coach`.

Ensure the required tables are created using the database schema definitions before running the application.

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
DB_HOST=localhost
DB_NAME=finance_coach
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

Keep your `.env` file private and do not commit credentials to GitHub.

---

## Running the Project

### Run the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

### Run the full statement upload pipeline

```bash
python -m ml.tests.test_statement_service
```

### Run individual module tests

```bash
python -m ml.tests.test_local_parser
python -m ml.tests.test_validator
python -m ml.tests.test_database
python -m ml.tests.test_spending_analysis
python -m ml.tests.test_anomaly_detection
python -m ml.tests.test_forecasting
python -m ml.tests.test_financial_insights
```

### Run the existing test suite

```bash
python -m ml.tests.test_all
```

---

## Sprint Roadmap

| Sprint | Scope | Status |
|---|---|---|
| Sprint 1 | PDF parsing, validation, PostgreSQL storage, audit logs | ✅ Complete |
| Sprint 2 | ML categorization, confidence scoring, feedback loop, dashboard | ✅ Implemented |
| Sprint 2 Validation | 500-row held-out evaluation and manual-labeling requirement | ⏳ Pending |
| Sprint 3 | Spending analysis, anomaly detection, forecasting, financial insights, dashboard integration | ✅ Implemented |
| Sprint 4 | Spring Boot REST API and backend integration | 🔜 Planned |
| Sprint 5 | JWT authentication, Docker, CI/CD, final testing and demo | 🔜 Planned |

---

## ML Validation

The expense categorization model uses **TF-IDF text features with a Random Forest classifier**.

The model supports eight categories:

- Food
- Rent
- Transport
- Entertainment
- Utilities
- Healthcare
- Shopping
- Others

### Current Development Result

On the 40-row India-specific development test set:

- Accuracy: **1.00**
- Weighted F1-score: **1.00**
- Test size: **40 transactions**
- 5 transactions per category

These are development results on a small dataset and should not be interpreted as evidence of generalization to unseen real-world bank statements.

The project also includes a feedback loop where user corrections are stored in PostgreSQL and can be incorporated into subsequent model retraining.

### Pending Acceptance Evaluation

The planned acceptance criterion is evaluation on a **500-row held-out labeled test set**. This evaluation has not yet been completed.

The current India-specific dataset also consists of programmatically generated examples rather than 200 genuinely manually labeled transactions. Therefore, the manual-labeling requirement remains pending.

---

## Security & Privacy

- Development uses synthetic and anonymized transaction data — no real personal financial information.
- `.env` is excluded from version control through `.gitignore`.
- Database transactions are used to prevent partial writes.
- Audit logs are maintained for data access and modification events.

---

## Internship Context

This project is developed as part of a **6-month software engineering internship** at **Persistent Systems**, under the mentorship of **Sneha Lodha**.

| | |
|---|---|
| **Institution** | Cummins College of Engineering for Women, Pune |
| **Program** | B.Tech Computer Engineering (2023–2027) |
| **Internship** | Persistent Systems — June 2026 |
| **Mentor** | Sneha Lodha, Persistent Systems |

---

## Author

**Akshita Totala**

B.Tech Computer Engineering, Cummins College of Engineering for Women, Pune

akshita.totala@cumminscollege.in

[GitHub](https://github.com/akshita-totala)
