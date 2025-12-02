import pandas as pd
from textblob import TextBlob


def analyze_sentiment(text):
    if pd.isna(text) or str(text).strip() == "":
        return "neutral", 0.0

    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        return "positive", polarity
    elif polarity < -0.1:
        return "negative", polarity
    else:
        return "neutral", polarity


def perform_sentiment_analysis(df):
    print("Analyzing sentiment for each review...")

    sentiments = []
    scores = []

    for i, review in enumerate(df['review']):
        sentiment, score = analyze_sentiment(review)
        sentiments.append(sentiment)
        scores.append(score)

        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1} reviews...")

    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores

    print(f"\nSentiment analysis complete!")
    print("Sentiment distribution:")
    print(df['sentiment_label'].value_counts())

    return df


def aggregate_by_bank_and_rating(df):
    """Calculate average sentiment for each bank and star rating"""
    print("\nAggregating sentiment by bank and rating...")

    results = []

    for bank in df['bank'].unique():
        for rating in [1, 2, 3, 4, 5]:
            mask = (df['bank'] == bank) & (df['rating'] == rating)
            bank_rating_reviews = df[mask]

            if len(bank_rating_reviews) > 0:
                avg_score = bank_rating_reviews['sentiment_score'].mean()
                sentiment_counts = bank_rating_reviews['sentiment_label'].value_counts(
                )

                results.append({
                    'bank': bank,
                    'rating': rating,
                    'avg_sentiment_score': round(avg_score, 3),
                    'positive_count': sentiment_counts.get('positive', 0),
                    'neutral_count': sentiment_counts.get('neutral', 0),
                    'negative_count': sentiment_counts.get('negative', 0),
                    'total_reviews': len(bank_rating_reviews)
                })

    aggregated_df = pd.DataFrame(results)
    print("Aggregation complete!")

    return aggregated_df
