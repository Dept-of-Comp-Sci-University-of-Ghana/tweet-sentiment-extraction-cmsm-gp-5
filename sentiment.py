import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re

# Load the CSV file into a DataFrame
df = pd.read_csv('test.csv')

# Function to clean the text by removing URLs and special characters, and converting to lowercase
def cleanTxt(text):
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text) 
    # Remove special characters, keeping only alphanumeric characters and spaces
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    return text

# Apply the cleanTxt function to the 'text' column
df['text'] = df['text'].apply(cleanTxt)

# Create an instance of SentimentIntensityAnalyzer for sentiment analysis
sid = SentimentIntensityAnalyzer()

# Function to get selected phrases based on sentiment
def getSelectedPhrases(text, sentiment):
    # Tokenize the text into individual words
    tokens = nltk.word_tokenize(text)
    # Use a set to automatically remove duplicate phrases
    phrases = set()
    # Loop through the tokens and create phrases of consecutive word pairs
    for i in range(len(tokens) - 1):
        phrase = tokens[i] + " " + tokens[i + 1]
        # Get the sentiment score of the phrase using SentimentIntensityAnalyzer
        sentiment_score = sid.polarity_scores(phrase)["compound"]
        # Check the sentiment condition and add the phrase to the set if it meets the criteria
        if sentiment == 'positive':
            if sentiment_score > 0:
                phrases.add(phrase)
        elif sentiment == 'negative':
            if sentiment_score < 0:
                phrases.add(phrase)
        else:
            # If sentiment is 'neutral', add the entire text as the phrase
            phrases.add(text)
    # Convert the set of phrases back to a list before returning
    return list(phrases)

# Apply the getSelectedPhrases function to each row of the DataFrame and create a new column 'new' to store the selected phrases
df['new'] = [getSelectedPhrases(row['text'], row['sentiment']) for _, row in df.iterrows()]

# Save the DataFrame to a new CSV file
df.to_csv('new.csv')

# Display the first few rows of the DataFrame to check the results
print(df.head())
