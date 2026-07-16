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

def insert_transaction(transaction):
    conn = connect_db()
    cur = conn.cursor()

    query = """
    INSERT INTO transactions
    (statement_id, user_id, date, description, amount, type)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    cur.execute(
        query,
        (
            None,
            None,
            transaction["date"],
            transaction["description"],
            transaction["amount"],
            transaction["type"].lower()
        )
    )

    conn.commit()

    cur.close()
    conn.close()