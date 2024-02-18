#pip install gensim

from gensim import models

# Train the LDA model
num_topics = 5  # Choose the number of topics
lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10, iterations=50)

# Print the topics and top words associated with each topic
for topic_id, topic_words in lda_model.print_topics():
    print(f'Topic {topic_id}: {topic_words}')