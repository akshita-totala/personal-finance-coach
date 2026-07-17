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
| PostgreSQL storage with audit logging | ✅ Complete |
| Duplicate statement detection | ✅ Complete |
| Graceful error handling | ✅ Complete |
| Test suite | ✅ Complete |
| Gemini AI integration (Q&A, smart parsing) | 🔄 Sprint 2 |
| Anomaly detection engine | 🔄 Sprint 2 |
| Monthly spend forecasting | 🔄 Sprint 3 |
| Streamlit dashboard | 🔄 Sprint 3 |
| Spring Boot REST API | 🔄 Sprint 4 |

---

## Tech Stack

**Current (Sprint 1)**
- Python 3.13
- PostgreSQL 18
- pdfplumber — PDF text extraction
- psycopg2 — PostgreSQL driver
- python-dotenv — environment configuration

**Planned (Sprint 2+)**
- Google Gemini API — AI-based parsing and Q&A
- scikit-learn — ML expense categorization
- Java Spring Boot — REST API layer
- Streamlit — analytics dashboard
- Docker + GitHub Actions — containerization and CI/CD

---

## Project Structure

```
personal-finance-coach/
│
├── backend/                    # Java Spring Boot API (Sprint 4)
├── dashboard/                  # Streamlit dashboard (Sprint 3)
├── database/
│   └── schema.sql              # PostgreSQL schema — all tables
│
├── ml/
│   ├── parser/
│   │   ├── local_parser.py     # pdfplumber-based PDF extraction
│   │   ├── parser_service.py   # Orchestrates parsing pipeline
│   │   ├── pdf_reader.py       # PDF file reading utilities
│   │   ├── prompts.py          # Prompt templates (for Gemini integration)
│   │   └── validator.py        # Transaction data validation rules
│   │
│   ├── services/
│   │   ├── db.py               # PostgreSQL connection and query helpers
│   │   └── statement_service.py # Statement upload, duplicate detection, audit logs
│   │
│   └── tests/
│       ├── test_database.py
│       ├── test_gemini.py
│       ├── test_local_parser.py
│       ├── test_parser_service.py
│       ├── test_pdf_reader.py
│       ├── test_statement_service.py
│       └── test_validator.py
│
├── sample_data/                # Synthetic bank statement PDFs for testing
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Database Schema

```sql
users          — registered users
statements     — uploaded PDF statements (with duplicate detection)
transactions   — extracted and categorized transactions
audit_logs     — all data access and modification events
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
Sprint 2 (Weeks 4–6)   🔄  Gemini API, ML categorization, anomaly detection
Sprint 3 (Weeks 7–9)   ⏳  Forecasting, Q&A engine, Streamlit dashboard
Sprint 4 (Weeks 10–12) ⏳  Spring Boot API, JWT auth, Docker, CI/CD
Sprint 5 (Weeks 13–14) ⏳  Testing, documentation, final demo
```

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