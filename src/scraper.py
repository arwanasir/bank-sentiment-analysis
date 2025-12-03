
import pandas as pd
from google_play_scraper import reviews, Sort
import time


def scrape_bank_reviews():

    bank_apps = {
        'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
        'Bank of Abyssinia': 'com.boa.boaMobileBanking',
        'Dashen Bank': 'com.dashen.dashensuperapp'
    }

    all_reviews = []
    TARGET_PER_BANK = 400

    for bank_name, app_id in bank_apps.items():
        print(f"Scraping reviews for {bank_name}...")
        bank_reviews = []
        continuation_token = None
        attempts = 0

        while len(bank_reviews) < TARGET_PER_BANK and attempts < 10:
            try:

                result, continuation_token = reviews(
                    app_id,
                    lang='en',
                    country='et',
                    sort=Sort.NEWEST,
                    count=200,
                    continuation_token=continuation_token
                )

                bank_reviews.extend(result)
                print(
                    f"  Batch: {len(result)} reviews, Total: {len(bank_reviews)}")

                if continuation_token is None:
                    break

            except Exception as e:
                print(f"  Error: {e}")
                break

            attempts += 1
            time.sleep(1)

        for review in bank_reviews[:TARGET_PER_BANK]:
            all_reviews.append({
                'review_id': review['reviewId'],
                'review': review['content'],
                'rating': review['score'],
                'date': review['at'].strftime('%Y-%m-%d'),
                'bank': bank_name,
                'source': 'Google Play'
            })

        collected = len(bank_reviews[:TARGET_PER_BANK])
        status = "YES" if collected >= TARGET_PER_BANK else "NO"
        print(f"{status} {bank_name}: {collected}/{TARGET_PER_BANK} reviews")

    df = pd.DataFrame(all_reviews)
    print(f"\nTOTAL COLLECTED: {len(df)} reviews")
    print("Distribution per bank:")
    print(df['bank'].value_counts())

    return df


if __name__ == "__main__":
    df = scrape_bank_reviews()
    df.to_csv('data/raw/raw_reviews.csv', index=False)
