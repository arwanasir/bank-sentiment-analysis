import pandas as pd
import numpy as np
from datetime import datetime


def preprocess_reviews(df):

    print("Starting data preprocessing...")
    print(f"Initial data shape: {df.shape}")

    initial_count = len(df)
    df = df.drop_duplicates(subset=['review_id'])
    print(f"Removed {initial_count - len(df)} duplicate reviews")

    missing_before = df.isnull().sum()
    df = df.dropna(subset=['review'])

    df['date'] = df['date'].fillna(pd.Timestamp.now().strftime('%Y-%m-%d'))

    print(
        f"Missing data handled. Removed {missing_before['review'] - df['review'].isnull().sum()} rows with missing reviews")

    try:
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Date formatting warning: {e}")

    print(f"Final data shape: {df.shape}")
    print(f"Reviews per bank:\n{df['bank'].value_counts()}")

    bank_counts = df['bank'].value_counts()
    for bank in ['Commercial Bank of Ethiopia', 'Bank of Abyssinia', 'Dashen Bank']:
        count = bank_counts.get(bank, 0)
        status = "YES" if count >= 400 else "NO"
        print(f"{status} {bank}: {count} reviews")

    return df


if __name__ == "__main__":
    df = pd.read_csv('data/raw/raw_reviews.csv')

    cleaned_df = preprocess_reviews(df)

    cleaned_df.to_csv('data/processed/cleaned_reviews.csv', index=False)
    print("Saved cleaned data to data/processed/cleaned_reviews.csv")
