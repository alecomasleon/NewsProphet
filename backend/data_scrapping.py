import requests
from bs4 import BeautifulSoup
from gensim import corpora, models
import nltk
from nltk.corpus import stopwords
import json

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Get English stopwords list
stop_words = set(stopwords.words('english'))

# Function to preprocess text data
def preprocess_text(text):
    # Tokenize the text (split into words)
    tokens = text.split()  # You may need a more sophisticated tokenizer depending on your requirements

    # Remove stopwords
    tokens = [token for token in tokens if token.lower() not in stop_words]

    # Optionally, you may perform additional text cleaning here

    return tokens

# Function to scrape article, preprocess data, and create bag-of-words representation
def scrape_and_preprocess_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting article metadata
    header = soup.find('h1').text.strip()
    body_text = ""
    for paragraph in soup.find_all('p'):
        body_text += paragraph.text.strip() + " "
    images = len(soup.find_all('img'))
    videos = len(soup.find_all('video'))
    num_paragraphs = len(soup.find_all('p'))
    references = [reference['href'] for reference in soup.find_all('a', href=True)]
    published_date = soup.find('meta', property='article:published_time')
    published_date = published_date['content'] if published_date else None

    # Preprocessing the text data
    preprocessed_text = preprocess_text(body_text)

    # Creating a dictionary from the preprocessed data
    dictionary = corpora.Dictionary([preprocessed_text])

    # Creating a bag-of-words representation of the article
    corpus = [dictionary.doc2bow(preprocessed_text)]

    # Combining metadata and preprocessed data
    article_data = {
        'header': header,
        'body': body_text,
        'num_images': images,
        'num_videos': videos, 
        'num_paragraphs': num_paragraphs,
        'references': references,
        'num_hyperlinks': len(references),
        'published_date': published_date,
        'preprocessed_text': preprocessed_text,
        'dictionary': dictionary,
        'corpus': corpus
    }

    return article_data

if __name__ == '__main__':
    url = 'https://www.wired.com/2014/03/everythingyoudidntknowyouwantedtoknow-about-the-science-of-cheese/'
    article_info = scrape_and_preprocess_article(url)

    # Remove Gensim dictionary object
    del article_info['dictionary']

    print(json.dumps(article_info, indent=4))

    # Load the Trained LDA Model
    lda_model_path = 'path_to_saved_model'  # Replace 'path_to_saved_model' with the actual path where you saved your trained LDA model file
    lda_model = models.LdaModel.load(lda_model_path)

    # Get the preprocessed text from the article_info dictionary
    preprocessed_text = article_info['preprocessed_text']

    # Infer topics for the preprocessed text using the trained LDA model
    bow_vector = article_info['corpus'][0]
    topic_distribution = lda_model[bow_vector]

    # Print the topic distribution
    print("Topic Distribution:")
    for topic_id, topic_prob in topic_distribution:
        print(f"Topic {topic_id}: {topic_prob}")

    # Interpretation: You can interpret the topic distribution to understand which topics are most relevant to the article's body.
