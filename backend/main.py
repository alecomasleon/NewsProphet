from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from data_scraping import scrape_article
import pandas as pd
from Scaler import Scaler
from get_features import get_features_from_article_data


app = Flask(__name__)
cors = CORS(app)

df = pd.read_csv('cleaned_extracted_data.csv')
df = df.drop('Unnamed: 0', axis=1)
Scaler = Scaler(df)
df = -1

model = -1

@app.route('/scrape', methods=["GET", "POST"])
def scrape():
    url = request.args.get('url')
    print("URL RECIEVED:" + url)

    return scrape_article(url)


@app.route('/calculate', methods=["GET", "POST"])
def news_score():
    print(request)

    article_data = request.args.get('article_data')
    features = get_features_from_article_data(article_data)
    score = model.predict(features)
    #maybe process

    return { 'score': score }


if __name__ == '__main__':
    app.run(debug=True, port=9000)