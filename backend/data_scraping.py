import requests
from bs4 import BeautifulSoup
import json

def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    header = soup.find('h1').text.strip()

    body = ""
    for paragraph in soup.find_all('p'):
        body += paragraph.text.strip() + "\n"

    images = len(soup.find_all('img'))

    num_paragraphs = len(soup.find_all('p'))

    references = []
    for reference in soup.find_all('a', href=True):
        references.append(reference['href'])

    num_hyperlinks = len(references)

    published_date = None
    if soup.find('meta', property='article:published_time'):
        published_date = soup.find('meta', property='article:published_time')['content']

    article_data = {
        'header': header,
        'body': body,
        'num_images': images,
        'num_paragraphs': num_paragraphs,
        'references': references,
        'num_hyperlinks': num_hyperlinks,
        'published_date': published_date
    }

    return article_data


if __name__ == '__main__':
    url = 'https://www.wired.com/2014/03/everythingyoudidntknowyouwantedtoknow-about-the-science-of-cheese/'
    article_info = scrape_article(url)
    print(json.dumps(article_info, indent=4))
