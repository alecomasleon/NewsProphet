import string
from mashable_url import make_valid_mashable_url
import nltk
from nltk.corpus import stopwords
from data_scraping import scrape_article
from datetime import datetime
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import PatternAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence


nltk.download('stopwords')

word_polarities = {}
classifier = TextClassifier.load('en-sentiment')

def get_flair_polarity(text):
    if text == '':
        return 0

    s = Sentence(text)
    classifier.predict(s)
    total_sentiment = s.labels[0]
    assert total_sentiment.value in ['POSITIVE', 'NEGATIVE']
    sign = 1 if total_sentiment.value == 'POSITIVE' else -1
    score = total_sentiment.score

    return sign * score


def get_polarity_and_sentiment(article_data, verbose=False, flair=True):
    body = article_data['body']
    body_sentiment = TextBlob(body, analyzer=PatternAnalyzer()).sentiment

    global_subjectivity = body_sentiment.subjectivity
    if flair:
        global_sentiment_polarity = get_flair_polarity(body)
    else:
        global_sentiment_polarity = body_sentiment.polarity

    body = body.lower()
    body = body.replace("'s", '')
    body = body.translate(str.maketrans("", "", string.punctuation))
    words = body.split(' ')
    words = [word for word in words if word not in stopwords.words('english')]

    neutral_threshold = 0.05
    num_pos_words = 0
    num_neg_words = 0
    num_non_neutral = 0
    sum_pos_polarity = 0
    max_positive_polarity = -1
    sum_neg_polarity = 0
    min_negative_polarity = 1

    for word in words:
        # print(word)
        if word in word_polarities:
            polarity = word_polarities[word]
        else:
            if flair:
                polarity = get_flair_polarity(word)
            else:
                polarity = TextBlob(body, analyzer=PatternAnalyzer()).sentiment.polarity
            word_polarities[word] = polarity
        
        if polarity > neutral_threshold:
            num_pos_words += 1
            num_non_neutral += 1
            sum_pos_polarity += polarity
            if polarity > max_positive_polarity:
                max_positive_polarity = polarity
        elif polarity < -neutral_threshold:
            num_neg_words += 1
            num_non_neutral += 1
            sum_neg_polarity += polarity
            if polarity < min_negative_polarity:
                min_negative_polarity = polarity

    
    if len(words) == 0:
        global_rate_positive_words = 0
        global_rate_negative_words = 0
    else:
        global_rate_positive_words = num_pos_words / len(words)
        global_rate_negative_words = num_neg_words / len(words)

    if num_non_neutral == 0:
        rate_positive_words = 0
        rate_negative_words = 0
    else:
        rate_positive_words = num_pos_words / num_non_neutral
        rate_negative_words = num_neg_words / num_non_neutral

    if num_pos_words == 0:
        avg_positive_polarity = 0
    else:
        avg_positive_polarity = sum_pos_polarity / num_pos_words
    
    if num_neg_words == 0:
        avg_negative_polarity = 0
    else:
        avg_negative_polarity = sum_neg_polarity / num_neg_words

    title = article_data['header']
    if verbose:
        print(title)
    title_sentiment = TextBlob(title, analyzer=PatternAnalyzer()).sentiment

    title_subjectivity = title_sentiment.subjectivity
    if flair:
        title_sentiment_polarity = get_flair_polarity(title)
    else:
        title_sentiment_polarity = title_sentiment.polarity

    abs_title_sentiment_polarity = abs(title_sentiment.polarity)

    polarity_and_sentiments = {
        'global_subjectivity': global_subjectivity,
        'global_sentiment_polarity': global_sentiment_polarity,
        'global_rate_positive_words': global_rate_positive_words,
        'global_rate_negative_words': global_rate_negative_words,
        'rate_positive_words': rate_positive_words,
        'rate_negative_words': rate_negative_words,
        'avg_positive_polarity': avg_positive_polarity,
        'max_positive_polarity': max_positive_polarity,
        'avg_negative_polarity': avg_negative_polarity,
        'min_negative_polarity': min_negative_polarity,
        'title_subjectivity': title_subjectivity,
        'title_sentiment_polarity': title_sentiment_polarity,
        'abs_title_sentiment_polarity': abs_title_sentiment_polarity
    }

    return polarity_and_sentiments


def get_token_features(article_data, verbose=False):
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


def get_features_from_article_data(article_data, verbose=False, do_flair=True):
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

    polarity_and_sentiments = get_polarity_and_sentiment(article_data, flair=do_flair)
    for i in polarity_and_sentiments.keys():
        features[i] = polarity_and_sentiments[i]

    X = pd.DataFrame(features, index=[0])

    if verbose:
        print(X.head())
        print(features)

    return X

if __name__=='__main__':
    get_features_from_article_data(scrape_article(make_valid_mashable_url('http://mashable.com/2013/01/14/twitter-mexico-violence/')))
