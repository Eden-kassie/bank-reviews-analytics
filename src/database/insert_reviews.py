# src/database/insert_reviews.py

import pandas as pd
from datetime import date
from .db_config import get_connection   

CSV_PATH = CSV_PATH = "analysis/data/play_reviews_sentiment_themes.csv"
  


def load_data():
    print(f"Loading data from: {CSV_PATH}")

    for enc in ["utf-8", "utf-8-sig", "latin-1"]:
        try:
            print(f"Trying encoding: {enc}")
            df = pd.read_csv(
                CSV_PATH,
                encoding=enc,
                sep=None,          # let pandas sniff the delimiter
                engine="python",   # required for sep=None
                on_bad_lines="warn"  # skip/flag weird lines, don't crash
            )
            print("✅ Read CSV successfully with encoding:", enc)
            print("Columns in CSV:", list(df.columns))
            print(df.head())
            return df
        except UnicodeDecodeError:
            print(f"❌ Unicode error with {enc}, trying next...")
        except Exception as e:
            print(f"❌ Parser error with {enc}: {e}")
            print("Trying next encoding...")

    raise RuntimeError(
        "Could not read CSV. Check the file format (delimiter/encoding) or re-save as a clean CSV."
    )




def get_bank_id_map(conn):
    """Return a dict mapping bank_name -> bank_id from DB."""
    cur = conn.cursor()
    cur.execute("SELECT bank_id, bank_name FROM banks;")
    rows = cur.fetchall()
    cur.close()

    mapping = {name: bank_id for bank_id, name in rows}
    print("Bank mapping from DB:", mapping)
    return mapping


def insert_reviews():
    df = load_data()

    print("Connecting to database...")
    conn = get_connection()
    cur = conn.cursor()

    bank_map = get_bank_id_map(conn)

    inserted = 0

    for idx, row in df.iterrows():
        bank_name = row["bank"]

        if bank_name not in bank_map:
            print(f"[Row {idx}] Warning: bank '{bank_name}' not found in banks table. Skipping.")
            continue

        bank_id = bank_map[bank_name]

        cur.execute(
            """
            INSERT INTO reviews
            (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                bank_id,
                row["review"],   # review text
                None,            # rating is missing in your CSV
                None,            # date is missing in your CSV
                row["sentiment_label"],
                float(row["sentiment_score"]) if not pd.isna(row["sentiment_score"]) else None,
                "google_play",
            ),
        )

        inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Done. Inserted {inserted} reviews into the database.")


if __name__ == "__main__":
    insert_reviews()
