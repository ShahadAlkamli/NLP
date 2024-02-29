# Import necessary libraries
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Load your dataset into a pandas DataFrame
file_path = '/Users/shahadsaeed/Desktop/preprocessed_tweets.csv'
df = pd.read_csv(file_path)

# Replace 'processed_tweet' with the actual column name in your CSV file that contains the tweet text
text_column = 'processed_tweet'

# Remove NaN values from the 'processed_tweet' column
df[text_column] = df[text_column].fillna('')  # Replace NaN with an empty string

# Function to perform sentiment analysis using TextBlob
def analyze_sentiment(tweet):
    analysis = TextBlob(str(tweet))  # Convert to string to handle NaN values
    return 'positive' if analysis.sentiment.polarity > 0 else 'negative' if analysis.sentiment.polarity < 0 else 'neutral'

# Apply the sentiment analysis function to each tweet in the dataset
df['Sentiment'] = df[text_column].apply(analyze_sentiment)

# Display the DataFrame with the sentiment column
print(df[[text_column, 'Sentiment']])

# Count the occurrences of each sentiment
sentiment_counts = df['Sentiment'].value_counts()

# 1. Plot the sentiment distribution
plt.figure(figsize=(8, 6), dpi=300)  # Increase dpi for better resolution
sentiment_counts.plot(kind='bar', color=['green', 'gray', 'red'])
plt.title('Sentiment Distribution of ChatGPT Privacy Tweets')
plt.xlabel('Sentiment')
plt.ylabel('Number of Tweets')

# Adjusting layout to prevent label cutting
plt.tight_layout()

# Save the figure with higher resolution
plt.savefig('/Users/shahadsaeed/Desktop/sentiment_distribution.png')
plt.close()

# 2. Plot a pie chart of sentiment proportions
plt.figure(figsize=(8, 8), dpi=300)  # Increase dpi for better resolution
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['green', 'gray', 'red'])
plt.title('Sentiment Proportions')

# Save the figure with higher resolution
plt.savefig('/Users/shahadsaeed/Desktop/sentiment_proportions.png')
plt.close()
