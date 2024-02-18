import requests
from bs4 import BeautifulSoup
from gensim import corpora
import nltk
from nltk.corpus import stopwords

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

    # Extract text from the article body
    body_text = ""
    for paragraph in soup.find_all('p'):
        body_text += paragraph.text.strip() + " "

    # Preprocess the text data
    preprocessed_text = preprocess_text(body_text)
    
    # Create a dictionary from the preprocessed data
    dictionary = corpora.Dictionary([preprocessed_text])
    
    # Create a bag-of-words representation of the article
    corpus = [dictionary.doc2bow(preprocessed_text)]
    
    return dictionary, corpus

if __name__ == '__main__':
    url = 'https://www.wired.com/2014/03/everythingyoudidntknowyouwantedtoknow-about-the-science-of-cheese/'
    dictionary, corpus = scrape_and_preprocess_article(url)
    print(dictionary)  # Print the dictionary
    print(corpus)  # Print the bag-of-words representation
