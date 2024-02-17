import string
from mashable_url import make_valid_mashable_url
import nltk
from nltk.corpus import stopwords
from data_scraping import scrape_article
from datetime import datetime
import pandas as pd


nltk.download('stopwords')

def get_token_features(article_data):
    body = article_data['body']
    body = body.lower()
    body = body.replace("'s", '')
    body = body.translate(str.maketrans("", "", string.punctuation))

    words = body.split(' ')
    unique_words = set(words)
    n_unique_tokens = len(unique_words)/len(words)

    num_non_stop_words = 0
    unique_non_stop_words = set()
    sum_word_len = 0

    stop_words = stopwords.words('english')

    for word in words:
        sum_word_len += len(word)
        if word not in stop_words:
            num_non_stop_words += 1
            unique_non_stop_words.add(word)
    
    average_token_length = sum_word_len/len(words)
    n_non_stop_words = num_non_stop_words / len(words)
    n_non_stop_unique_tokens = len(unique_non_stop_words)

    token_features = {
        'n_unique_tokens': n_unique_tokens,
        'n_non_stop_words': n_non_stop_words,
        'n_non_stop_unique_tokens': n_non_stop_unique_tokens,
        'average_token_length': average_token_length
    }

    return token_features


def get_features_from_article_data(article_data):
    features = {}
    features['n_tokens_title'] = len(article_data['header'].split(' '))
    features['n_tokens_content'] = len(article_data['body'].split(' '))

    token_features = get_token_features(article_data)

    features['n_unique_tokens'] = token_features['n_unique_tokens']
    features['n_non_stop_words'] = token_features['n_non_stop_words']
    features['n_non_stop_unique_tokens'] = token_features['n_non_stop_unique_tokens']

    features['num_hrefs'] = article_data['num_hyperlinks']
    features['num_imgs'] = article_data['num_images']
    features['num_videos'] = article_data['num_videos']

    features['average_token_length'] = token_features['average_token_length']

    # 19-27

    format_data = "%Y-%m-%d"
    date = datetime.strptime(article_data['published_date'][:10], format_data)
    weekday = date.weekday()
    features['weekday_is_monday'] = 1 if weekday == 0 else 0
    features['weekday_is_tuesday'] = 1 if weekday == 1 else 0
    features['weekday_is_wednesday'] = 1 if weekday == 2 else 0
    features['weekday_is_thursday'] = 1 if weekday == 3 else 0
    features['weekday_is_friday'] = 1 if weekday == 4 else 0
    features['weekday_is_saturday'] = 1 if weekday == 5 else 0
    features['weekday_is_sunday'] = 1 if weekday == 6 else 0
    features['is_weekend'] = 1 if weekday == 5 or weekday == 6 else 0

    # LDA
    # subjectivity, sentiment

    X = pd.DataFrame(features, index=[0])

    print(X.head())

    return X

if __name__=='__main__':
    get_features_from_article_data(scrape_article(make_valid_mashable_url('http://mashable.com/2013/01/17/80s-video-dating/')))
