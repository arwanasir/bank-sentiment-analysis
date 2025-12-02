import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re


def extract_keywords(reviews, top_n=20):
    print("Extracting important keywords...")

    clean_reviews = []
    for review in reviews:
        if pd.isna(review):
            clean_reviews.append("")
        else:
            text = str(review).lower()
            text = re.sub(r'[^\w\s]', ' ', text)
            clean_reviews.append(text)

    vectorizer = TfidfVectorizer(
        max_features=top_n,
        stop_words='english',
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(clean_reviews)
    feature_names = vectorizer.get_feature_names_out()

    print(f"Found {len(feature_names)} keywords")
    return feature_names


def group_into_themes(keywords):
    """Group keywords into 3-5 themes manually"""
    print("\nGrouping keywords into themes...")

    themes = {
        'Login & Account Access': [],
        'Transaction & Transfer': [],
        'App Performance': [],
        'User Interface': [],
        'Customer Support': [],
        'Feature Requests': []
    }

    login_words = ['login', 'password', 'fingerprint', 'access', 'account']
    transaction_words = ['transfer', 'transaction', 'money', 'send', 'payment']
    performance_words = ['slow', 'fast', 'crash', 'error', 'bug', 'work']
    ui_words = ['interface', 'design', 'easy', 'simple', 'beautiful']
    support_words = ['support', 'help', 'service', 'contact']
    feature_words = ['should', 'could', 'please', 'add', 'feature']

    for keyword in keywords:
        keyword_lower = keyword.lower()

        if any(word in keyword_lower for word in login_words):
            themes['Login & Account Access'].append(keyword)
        elif any(word in keyword_lower for word in transaction_words):
            themes['Transaction & Transfer'].append(keyword)
        elif any(word in keyword_lower for word in performance_words):
            themes['App Performance'].append(keyword)
        elif any(word in keyword_lower for word in ui_words):
            themes['User Interface'].append(keyword)
        elif any(word in keyword_lower for word in support_words):
            themes['Customer Support'].append(keyword)
        elif any(word in keyword_lower for word in feature_words):
            themes['Feature Requests'].append(keyword)
        else:
            for theme in themes:
                if len(themes[theme]) < 5:
                    themes[theme].append(keyword)
                    break

    themes = {k: v for k, v in themes.items() if v}

    print(f"Created {len(themes)} themes")
    for theme, words in themes.items():
        print(f"  {theme}: {', '.join(words[:5])}")

    return themes


def analyze_themes_by_bank(df):
    print("\n" + "="*50)
    print("THEMATIC ANALYSIS BY BANK")
    print("="*50)

    bank_themes = {}

    for bank in df['bank'].unique():
        print(f"\nAnalyzing {bank}...")

        bank_reviews = df[df['bank'] == bank]['review'].tolist()
        keywords = extract_keywords(bank_reviews)

        themes = group_into_themes(keywords)
        theme_examples = {}
        for theme, theme_keywords in themes.items():
            examples = []
            for review in bank_reviews[:20]:
                if any(keyword in str(review).lower() for keyword in theme_keywords[:3]):
                    short_review = str(review)[
                        :80] + "..." if len(str(review)) > 80 else str(review)
                    examples.append(short_review)
                    if len(examples) >= 2:
                        break
            theme_examples[theme] = examples

        bank_themes[bank] = {
            'themes': themes,
            'examples': theme_examples
        }

        print(f"{bank}: Found {len(themes)} themes")

    return bank_themes
