import pandas as pd

INPUT_PATH = "data/raw/reviews_raw.csv"
OUTPUT_PATH = "data/processed/bank_reviews_clean.csv"

def preprocess_reviews():
    df = pd.read_csv(INPUT_PATH, parse_dates=["date"])

    # Remove missing or empty reviews
    df = df.dropna(subset=["review", "rating"])
    df["review"] = df["review"].astype(str).str.strip()

    # Remove duplicate reviews
    df = df.drop_duplicates(subset=["bank", "review"])

    # Normalize dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    df = df[["review", "rating", "date", "bank", "source"]]

    print("Clean rows:", len(df))
    print("\nRows per bank:\n", df["bank"].value_counts())

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved cleaned data → {OUTPUT_PATH}")


if __name__ == "__main__":
    preprocess_reviews()
