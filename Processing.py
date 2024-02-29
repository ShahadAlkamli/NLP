import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Load your CSV file containing tweets from the desktop
input_file_path = '/Users/shahadsaeed/Desktop/ChatGPTtweets.csv'
df = pd.read_csv(input_file_path)

# Preprocessing
def preprocess_text(text):
    # Check if the text is NaN, and if so, return empty strings
    if pd.isna(text):
        return '', ''
    
    # Convert text to lowercase for consistent analysis
    text_lower = text.lower()
    # Remove hyperlinks from the text
    text_no_links = re.sub(r'http\S+', '', text_lower)
    # Remove mentions
    text_no_mentions = re.sub(r'@\w+', '', text_no_links)
    
    # Tokenize the text into individual words
    tokens = word_tokenize(text_no_mentions)
    # Remove common stop words that don't carry much meaning
    stop_words = set(stopwords.words('english'))
    tokens_no_stopwords = [word for word in tokens if word.isalpha() and word not in stop_words]
    # Join the processed tokens into a string
    processed_text = ' '.join(tokens_no_stopwords)
    
    # Additional preprocessing for data security and privacy
    relevant_keywords = ['security', 'privacy', 'cybersecurity', 'confidentiality', 'secure', 'hack', 'hacker', 'encryption', 'theft']
    
    if any(keyword in processed_text.lower() for keyword in relevant_keywords):
        return text, processed_text
    else:
        # Return empty strings if the tweet is not relevant
        return None, None

# Apply preprocessing to each tweet and create new columns 'original_tweet' and 'processed_tweet'
df['original_tweet'], df['processed_tweet'] = zip(*df['content'].apply(preprocess_text))

# Filter out rows where both 'original_tweet' and 'processed_tweet' are empty
df = df.dropna(subset=['original_tweet', 'processed_tweet'])

# Save preprocessed data to a new CSV file on the desktop
output_file_path = '/Users/shahadsaeed/Desktop/preprocessed_privacy_tweets.csv'
df.to_csv(output_file_path, columns=['original_tweet', 'processed_tweet'], index=False)
