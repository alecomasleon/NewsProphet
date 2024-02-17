import re

from data_scraping import scrape_article


def make_valid_mashable_url(original_url):
    new_url = re.sub('[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]', 'archive', original_url)

    return new_url


if __name__ == '__main__':
    print(make_valid_mashable_url('http://mashable.com/2013/01/17/80s-video-dating/'))
    print(scrape_article(make_valid_mashable_url('https://mashable.com/archive/smartbash-ces-2013')))