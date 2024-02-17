def get_token_features(article_data):
    body = article_data['body']


def get_features_from_article_data(article_data):
    article_data = {
        'header': header,
        'body': body,
        'num_images': images,
        'num_paragraphs': num_paragraphs,
        'references': references,
        'num_hyperlinks': num_hyperlinks,
        'published_date': published_date
    }
    features = {}
    features['n_tokens_title'] = len(article_data['header'].split(' '))
    features['n_tokens_content'] = len(article_data['body'].split(' '))

    # 4. n_unique_tokens:               Rate of unique words in the content
    # 5. n_non_stop_words:              Rate of non-stop words in the content
    # 6. n_non_stop_unique_tokens:      Rate of unique non-stop words in the content

    features['num_hrefs'] = article_data['num_hyperlinks']
    features['num_imgs'] = article_data['num_images']
    features['num_videos'] = article_data['num_videos']

    # 11. average_token_length:          Average length of the words in the content
    