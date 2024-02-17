from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from data_scraping import scrape_article


app = Flask(__name__)
cors = CORS(app)

@app.route('/scrape', methods=["GET", "POST"])
def scrape():
    url = request.args.get('url')
    print("URL RECIEVED:" + url)

    return scrape_article(url)


@app.route('/news_score', methods=["GET", "POST"])
def news_score():
    print(request)
    # get_features
    # input to model
    #maybe process
    # return some score
    return 'news_score'


if __name__ == '__main__':
    app.run(debug=True, port=9000)