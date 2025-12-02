import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def create_database():
    """Create database if it doesn't exist"""
    # Connect to default 'postgres' database
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',  # Connect to default DB
        user='postgres',
        password='arwa4063',  # Your password
        port='5432'
    )
    conn.autocommit = True  # Need this for CREATE DATABASE
    cur = conn.cursor()

    # Check if database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'bank_reviews'")
    exists = cur.fetchone()

    if not exists:
        cur.execute("CREATE DATABASE bank_reviews")
        print("✅ Created 'bank_reviews' database")
    else:
        print("✅ 'bank_reviews' database already exists")

    cur.close()
    conn.close()


def setup_database():
    """Create database and tables"""
    create_database()
    conn = psycopg2.connect(
        host='localhost',
        database='bank_reviews',
        user='postgres',
        password='arwa4063',
        port='5432'
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(100) NOT NULL,
            app_name VARCHAR(100)
        );
        
        CREATE TABLE IF NOT EXISTS reviews (
            review_id VARCHAR(100) PRIMARY KEY,
            bank_id INTEGER REFERENCES banks(bank_id),
            review_text TEXT,
            rating INTEGER CHECK (rating >= 1 AND rating <= 5),
            review_date DATE,
            sentiment_label VARCHAR(20),
            sentiment_score FLOAT,
            source VARCHAR(50)
        );
    """)

    # Insert banks
    banks = [
        ('Commercial Bank of Ethiopia', 'CBE Mobile'),
        ('Bank of Abyssinia', 'BOA Mobile Banking'),
        ('Dashen Bank', 'Dashen SCMobile')
    ]
    cur.executemany(
        "INSERT INTO banks (bank_name, app_name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        banks
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Database setup complete")


def insert_reviews():
    """Insert cleaned reviews"""
    df = pd.read_csv('../data/processed/cleaned_reviews.csv')

    conn = psycopg2.connect(
        host='localhost',
        database='bank_reviews',
        user='postgres',
        password='arwa4063',
        port='5432'
    )
    cur = conn.cursor()

    # Get bank IDs from database
    cur.execute("SELECT bank_name, bank_id FROM banks")
    bank_ids = {row[0]: row[1] for row in cur.fetchall()}

    # Create normalized mapping (lowercase for case-insensitive comparison)
    normalized_bank_ids = {}
    for name, bank_id in bank_ids.items():
        normalized_name = name.lower().strip()
        normalized_bank_ids[normalized_name] = bank_id

    records = []
    unmatched_banks = set()

    for _, row in df.iterrows():
        csv_bank = str(row['bank']).strip()
        normalized_csv_bank = csv_bank.lower().strip()

        bank_id = normalized_bank_ids.get(normalized_csv_bank)

        if bank_id:
            records.append((
                str(row['review_id']),
                bank_id,
                str(row['review']),
                int(row['rating']),
                row['date'],
                'unknown',
                0.0,
                'Google Play'
            ))
        else:
            unmatched_banks.add(csv_bank)

    # Warn about any unmatched banks
    if unmatched_banks:
        print(
            f"⚠️  Warning: These banks in CSV don't match database: {unmatched_banks}")

    # Insert all records
    if records:
        insert_query = "INSERT INTO reviews VALUES %s ON CONFLICT DO NOTHING"
        execute_values(cur, insert_query, records)
        conn.commit()

    print(f"✅ Inserted {len(records)} reviews")

    cur.close()
    conn.close()
    return len(records)


def verify_data():
    """Verify data integrity"""
    conn = psycopg2.connect(
        host='localhost',
        database='bank_reviews',
        user='postgres',
        password='arwa4063',
        port='5432'
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM reviews")
    total = cur.fetchone()[0]

    cur.execute("SELECT b.bank_name, COUNT(r.review_id) FROM banks b LEFT JOIN reviews r ON b.bank_id = r.bank_id GROUP BY b.bank_name")

    print(f"\n📊 Total reviews: {total}")
    print("Reviews per bank:")
    for bank, count in cur.fetchall():
        print(f"  {bank}: {count}")

    cur.close()
    conn.close()
    return total
