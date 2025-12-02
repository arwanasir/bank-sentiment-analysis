# bank-sentiment-analysis

# Project Overview

Analysis of user reviews for three Ethiopian banking apps to identify satisfaction drivers and pain points.

# Banks Analyzed

Commercial Bank of Ethiopia (CBE)
Bank of Abyssinia (BOA)
Dashen Bank

# Methodology

Data Collection: Scraped 1,200+ reviews from Google Play Store
Preprocessing: Removed duplicates, handled missing data, standardized formats
Sentiment Analysis: Used TextBlob for sentiment classification
Thematic Analysis: TF-IDF and keyword-based theme extraction
Key Findings
CBE has highest positive sentiment
Transaction speed is major concern across all banks
Login authentication issues most common for BOA
Feature requests focus on biometric login and faster transfers
File Structure

## Database Setup (Task 3)

### Prerequisites

1. Install PostgreSQL: https://www.postgresql.org/download/
2. Start PostgreSQL service
3. Create database: `createdb bank_reviews`

### Setup

1. Copy `.env.example` to `.env` and update credentials
2. Install dependencies: `pip install -r requirements_db.txt`
3. Run setup: `python src/database.py`

### Database Schema

```sql
-- Banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100)
);

-- Reviews table
CREATE TABLE reviews (
    review_id VARCHAR(100) PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    source VARCHAR(50)
);
```
