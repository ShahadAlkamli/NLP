import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# Load your preprocessed CSV file
input_file_path = '/Users/shahadsaeed/Desktop/preprocessed_tweets.csv'
df = pd.read_csv(input_file_path)

# Filter out rows with missing 'processed_tweet'
df = df.dropna(subset=['processed_tweet'])

# Use the 'processed_tweet' column directly for LDA
corpus = [text.split() for text in df['processed_tweet']]

# Create a dictionary representation of the documents
dictionary = corpora.Dictionary(corpus)

# Create a document-term matrix
corpus = [dictionary.doc2bow(tokens) for tokens in corpus]

# Build the LDA model
num_topics = 10  # Set the number of topics
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

# Extract and print the topics
topics = lda_model.show_topics(num_words=10, formatted=False)
for topic_num, words in topics:
    print(f"Topic: {topic_num}")
    print(f"Words: {', '.join([word[0] for word in words])}\n")

# Visualize topics with a Word Cloud
topics = []
for topic_id in range(num_topics):
    topic_words = lda_model.show_topic(topic_id, topn=10)
    words = [word for word, _ in topic_words if word in dictionary.token2id]
    topics.append(words)

# Flatten the list of words
all_words = [word for sublist in topics for word in sublist]

# Concatenate all words into a single string
text = ' '.join(all_words)

# Generate a word cloud image
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the generated image using Matplotlib with increased resolution (dpi)
plt.figure(figsize=(10, 5), dpi=300)  # Adjust the dpi parameter
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Visualize topics distribution
# Get topic distribution for each document
topics_distribution = [lda_model[doc] for doc in corpus]

# Extract the dominant topic for each document
dominant_topics = [max(topic, key=lambda x: x[1])[0] for topic in topics_distribution]

# Count the occurrences of each dominant topic
topic_counts = pd.Series(dominant_topics).value_counts().sort_index()

# Visualize the distribution of dominant topics using a bar chart
plt.figure(figsize=(10, 6), dpi=300)  # Adjust the dpi parameter
sns.barplot(x=topic_counts.index, y=topic_counts.values, palette='viridis')
plt.title('Dominant Topic Distribution')
plt.xlabel('Dominant Topic')
plt.ylabel('Number of Tweets')
plt.show()
