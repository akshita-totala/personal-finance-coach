import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def log_event(action, resource, user_id=None):
    conn = connect_db()
    cur = conn.cursor()

    query = """
    INSERT INTO audit_logs (user_id, action, resource)
    VALUES (%s, %s, %s)
    """

    cur.execute(
        query,
        (
            user_id,
            action,
            resource
        )
    )

    conn.commit()

    cur.close()
    conn.close()

def statement_exists(filename):
    conn = connect_db()
    cur = conn.cursor()

    query = """
    SELECT EXISTS(
        SELECT 1
        FROM statements
        WHERE filename = %s
    )
    """

    cur.execute(query, (filename,))

    exists = cur.fetchone()[0]

    cur.close()
    conn.close()

    return exists

def insert_statement(filename):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO statements (filename, status)
        VALUES (%s, %s)
        RETURNING id;
    """, (filename, "processed"))

    statement_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return statement_id

def insert_transaction(transaction, statement_id):
    conn = connect_db()
    cur = conn.cursor()

    query = """
    INSERT INTO transactions
    (statement_id, user_id, date, description, amount, type, category)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    cur.execute(
        query,
        (
            statement_id,
            None,
            transaction["date"],
            transaction["description"],
            transaction["amount"],
            transaction["type"].lower(),
            transaction["category"]
        )
    )

    conn.commit()

    cur.close()
    conn.close()