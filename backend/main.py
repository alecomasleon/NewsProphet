import pickle
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from data_scraping import scrape_article
import pandas as pd
from Scaler import Scaler
from get_features import get_features_from_article_data
import json
import sklearn

import openai

openai.api_key = "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"
CHAT_GPT = False
chat_gpt = openai.OpenAI(api_key=openai.api_key)

print(sklearn.__version__)
app = Flask(__name__)
cors = CORS(app)

df = pd.read_csv('backend/model_creation/cleaned_extracted_data.csv')
df = df.drop('Unnamed: 0', axis=1)
Scaler = Scaler(df)
df = -1

with open('backend/model.pkl', 'rb') as file:
    model = pickle.load(file)
    # print(model)

@app.route('/scrape', methods=["GET", "POST"])
def scrape():
    url = request.args.get('url')
    print("URL RECIEVED:" + url)

    return scrape_article(url)


@app.route('/calculate', methods=["GET", "POST"])
def news_score():
    print('CALCULATE')

    article_data = {}
    lst_args = ['header', 'body', 'num_images', 'num_hyperlinks', 'num_videos', 'published_date']
    for arg in lst_args:
        article_data[arg] = request.args.get(arg)
    print('DATA GOTTEN')
    print(article_data)
    features = get_features_from_article_data(article_data)
    print('FEATURES_GOTTEN')
    scaled_features = Scaler.transform(features)
    print(scaled_features)
    score = model.predict(scaled_features)[0]
    # score = -200

    print('Score: ' + str(score))

    # process
    msg = process(features, scaled_features, score)

    print(msg)

    return msg
    # return jsonify(features)


def process(features, scaled_features, score):
    msg = ''
    # global_subjectivity
    if features['global_subjectivity'][0] > 0.8:
        msg += 'Your article has a subjectivity score of ' + str(round(features['global_subjectivity'][0], 2)) + ', which is very subjective. '
    elif features['global_subjectivity'][0] > 0.5:
        msg += 'Your article has a subjectivity score of ' + str(round(features['global_subjectivity'][0], 2)) + ', which is slightly subjective. '
    elif features['global_subjectivity'][0] < -0.8:
        msg += 'Your article has a subjectivity score of ' + str(round(features['global_subjectivity'][0], 2)) + ', which is very objective. '
    elif features['global_subjectivity'][0] < -0.5:
        msg += 'Your article has a subjectivity score of ' + str(round(features['global_subjectivity'][0], 2)) + ', which is slightly objective. '

    # global_sentiment_polarity
    if features['global_sentiment_polarity'][0] > 0.9:
        msg += 'It has a very positive sentiment score of ' + str(round(features['global_sentiment_polarity'][0], 2)) + '. '
    elif features['global_sentiment_polarity'][0] > 0.7:
        msg += 'It has a slightly positive sentiment score of ' + str(round(features['global_sentiment_polarity'][0], 2)) + '. '
    elif features['global_sentiment_polarity'][0] < 0.1:
        msg += 'It has a very negative sentiment score of ' + str(round(features['global_sentiment_polarity'][0], 2)) + '. '
    elif features['global_sentiment_polarity'][0] < 0.3:
        msg += 'It has a slightly negative sentiment score of ' + str(round(features['global_sentiment_polarity'][0], 2)) + '. '
        
    # global_rate_positive_words
    if scaled_features['global_rate_positive_words'][0] > 1:
        msg += "Has a high rate of positive words. "
    
    # global_rate_negative_words
    if scaled_features['global_rate_negative_words'][0] > 1:
        msg += "Has a high rate of negative words. "
    
    if msg != '':
        msg += '\n'

    # title_subjectivity
    if scaled_features['title_subjectivity'][0] > 1:
        msg += 'Title is very subjective. '
    elif scaled_features['title_subjectivity'][0] < -1:
        msg += 'Title is very objective. '
    
    # title_sentiment_polarity
    if scaled_features['title_sentiment_polarity'][0] > 1:
        msg += 'Title is very positive. '
    elif scaled_features['title_sentiment_polarity'][0] < -1:
        msg += 'Title is very negative. '
    
    if msg == '':
        msg = 'Article is very neutral.'
    
    if CHAT_GPT:
        prompt = 'Slightly paraphrase these scentences, using the same numbers: "' + msg + '"'
        name = "gpt-3.5-turbo"
        # name = "babbage-002"
        # name = "whisper-1"
        response = chat_gpt.chat.completions.create(model=name, messages=[{'role':"system", 'content': prompt}], max_tokens=len(prompt.split(' ')))
        msg = response.choices[0].text

    details = {}
    for col in features.columns:
        # print(type(features[col][0].item()))
        details[col] = round(features[col][0].item(), 3)
    details['score'] = score
    
    print(details)
    score_msg = "NewsProphet predicts your news shares score will be: " + str(round(score, 3)) + '.'

    return {'score_msg': score_msg, 'msg': msg, 'details': json.dumps(details)}


if __name__ == '__main__':
    app.run(debug=True, port=9000)