# Personal Finance Coach

> An AI-assisted backend system that extracts, validates, categorizes, and stores bank transactions from PDF statements — built as part of a software engineering internship at **Persistent Systems**.

---

## Overview

Most individuals have no real-time visibility into their spending. Bank statements exist as unreadable PDFs, and manual tracking is tedious and error-prone.

The **Personal Finance Coach** solves this by automating the entire pipeline — from PDF ingestion to structured, categorized transaction data stored in a relational database — laying the foundation for AI-powered financial insights.

---

## Features

| Feature | Status |
|---|---|
| PDF bank statement parsing | ✅ Complete |
| Transaction extraction & structuring | ✅ Complete |
| Data validation (date, amount, type) | ✅ Complete |
| Automatic expense categorization | ✅ Complete |
| ML confidence scoring | ✅ Complete |
| Manual category correction | ✅ Complete |
| Feedback storage & feedback-based retraining | ✅ Complete |
| PostgreSQL storage with audit logging | ✅ Complete |
| Duplicate statement detection | ✅ Complete |
| Graceful error handling | ✅ Complete |
| Streamlit dashboard | ✅ Complete |
| Spending summary & category visualization | ✅ Complete |
| End-to-end statement upload pipeline | ✅ Complete |
| 500-row held-out ML evaluation | ⏳ Pending |
| Genuine/manual labeling requirement | ⏳ Pending |
| Anomaly detection engine | 🔄 Sprint 3 |
| Monthly spend forecasting | 🔄 Sprint 3 |
| Spring Boot REST API | 🔄 Sprint 4 |

## Tech Stack

**Current**

- Python 3.13
- PostgreSQL 18
- pdfplumber — PDF text extraction
- psycopg2 — PostgreSQL driver
- python-dotenv — environment configuration
- scikit-learn — ML expense categorization
- Streamlit — analytics dashboard
- joblib — model persistence

**Planned**

- Java Spring Boot — REST API layer
- Docker + GitHub Actions — containerization and CI/CD

## Project Structure

```text
personal-finance-coach/

├── backend/
│   └── # Java Spring Boot API (Sprint 4)

├── dashboard/
│   └── app.py                    # Streamlit dashboard

├── database/
│   └── schema.sql                # PostgreSQL schema

├── ml/
│   ├── models/
│   │   ├── categorizer_model.pkl
│   │   ├── tfidf_vectorizer.pkl
│   │   ├── train_categorizer.py
│   │   ├── predict_categorizer.py
│   │   ├── retrain_from_feedback.py
│   │   └── test_india_model.py
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
│   │   └── test_validator.py
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

## Database Schema

```sql
users         — registered users
statements    — uploaded PDF statements
transactions  — extracted and categorized transactions
audit_logs    — data access and modification events
feedback      — user category corrections used for model improvement
```

Full schema: [`database/schema.sql`](database/schema.sql)

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 16+
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
Create a PostgreSQL database named `finance_coach`, then run:
```bash
psql -U postgres -d finance_coach -f database/schema.sql
```

### 4. Configure environment
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key
DB_HOST=localhost
DB_NAME=finance_coach
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## Running the Project

**Run the full statement upload pipeline:**
```bash
python -m ml.tests.test_statement_service
```

**Run individual module tests:**
```bash
python -m ml.tests.test_local_parser
python -m ml.tests.test_validator
python -m ml.tests.test_database
```

**Run all tests:**
```bash
python -m ml.tests.test_all
```

---

## Sprint Roadmap

```
Sprint 1 (Weeks 1–3)   ✅  PDF parsing, validation, DB storage, audit logs

Sprint 2 (Weeks 4–6)   ✅  ML categorization, feedback loop,
                            Streamlit dashboard

Sprint 2 validation     ⏳  500-row held-out evaluation and
                            manual-labeling requirement

Sprint 3 (Weeks 7–9)    ⏳  Anomaly detection, forecasting,
                            Spring Boot API

Sprint 4 (Weeks 10–12) ⏳  JWT authentication, Docker, CI/CD

Sprint 5 (Weeks 13–14) ⏳  Testing, documentation, final demo
```
## ML Validation

The current expense categorization model uses TF-IDF text features with a Random Forest classifier.

The model supports the following categories:

- Food
- Rent
- Transport
- Entertainment
- Utilities
- Healthcare
- Shopping
- Others

### Current Development Result

On the locked 40-row India-specific development test set:

- Accuracy: **1.00**
- Weighted F1-score: **1.00**
- Test size: **40 transactions**
- 5 transactions per category

The project also includes a feedback loop where user corrections are stored in PostgreSQL and incorporated into subsequent model retraining.

### Pending Acceptance Evaluation

The planned acceptance criterion is evaluation on a **500-row held-out labeled test set**. This evaluation has not yet been completed.

The current India-specific dataset also consists of programmatically generated examples rather than 200 genuinely manually labeled transactions, so the manual-labeling requirement remains pending.
---

## Security & Privacy

- All development uses **synthetic and anonymized** transaction data — no real PII
- `.env` file excluded from version control via `.gitignore`
- Database transactions used to prevent partial writes
- Audit logs maintained for all data access events

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