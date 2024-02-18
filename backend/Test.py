from numba import jit, cuda
import numpy as np
# to measure exec time
from timeit import default_timer as timer   
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages/')
sys.path.append('/backend/model_creation')

from ucimlrepo import fetch_ucirepo
from data_scraping import scrape_article
from get_features import get_features_from_article_data
from mashable_url import make_valid_mashable_url
import pandas as pd
import get_features
 
# function optimized to run on gpu 
@jit(target_backend='cuda')                         
def func2():
    from ucimlrepo import fetch_ucirepo
    from data_scraping import scrape_article
    from get_features import get_features_from_article_data
    from mashable_url import make_valid_mashable_url
    import pandas as pd
    import get_features
    online_news_popularity = fetch_ucirepo(id=332)
    data = online_news_popularity.data.original
    urls = data['url'].to_list()
    y = online_news_popularity.data.targets

    get_features.word_polarities = {}
    length = len(urls)
    # length = 20
    df = pd.DataFrame()
    for i in range(length):
        print(str(i+1) + '/' + str(length))
        entry = get_features_from_article_data(scrape_article(make_valid_mashable_url(urls[i])), do_flair=False)
        df = pd.concat([df, entry], ignore_index=True)
    
    return df

if __name__=="__main__":     
    start = timer()
    df = func2()
    print("with GPU:", timer()-start)
    print(df.head())
    df.to_csv('raw_extracted_data.csv')