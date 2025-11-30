import pandas as pd
import re
import os

RAW_PATH = "scrape_output/merged_play_reviews.csv"
CLEAN_PATH = "scrape_output/cleaned_play_reviews.csv"

def clean_text(text):
    if pd.isna(text):
        return ""

    text = text.lower()                              # lowercase
    text = re.sub(r'\n', ' ', text)                  # remove newlines
    text = re.sub(r'[^a-z0-9\s.,!?]', '', text)      # keep letters/numbers/punctuation
    text = re.sub(r'\s+', ' ', text).strip()         # remove extra spaces
    return text

def preprocess():
    print("🔄 Loading data...")

    df = pd.read_csv(RAW_PATH)

    print("Initial rows:", len(df))

    # ---------------------------
    # 1. Remove duplicates
    # ---------------------------
    df.drop_duplicates(subset=["review_id"], inplace=True)

    # ---------------------------
    # 2. Clean review text
    # ---------------------------
    df["content_clean"] = df["content"].astype(str).apply(clean_text)

    # ---------------------------
    # 3. Handle missing values
    # ---------------------------
    df.fillna({
        "content": "",
        "content_clean": "",
        "reply_content": "",
        "review_created_version": ""
    }, inplace=True)

    # Convert dates
    df["at"] = pd.to_datetime(df["at"], errors="coerce")
    df["replied_at"] = pd.to_datetime(df["replied_at"], errors="coerce")

    # ---------------------------
    # 4. Add length of review
    # ---------------------------
    df["review_length"] = df["content_clean"].apply(lambda x: len(x.split()))

    print("Final rows:", len(df))

    # Save cleaned CSV
    df.to_csv(CLEAN_PATH, index=False)

    print("✅ Saved cleaned dataset to:", CLEAN_PATH)


if __name__ == "__main__":
    preprocess()
