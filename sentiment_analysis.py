import pandas as pd
import string
import re
from nltk.stem import WordNetLemmatizer

# Load stopwords manually from file
stopwords_path = "C:/Users/Varad/AppData/Roaming/nltk_data/corpora/stopwords/english"
with open(stopwords_path, encoding="utf8") as f:
    stop_words = set(f.read().splitlines())

lemmatizer = WordNetLemmatizer()

# Sample data
data = {
    'text': [
        "I love this product! It's amazing 😍",
        "This is the worst experience I've had.",
        "Not bad, could be better.",
        "Absolutely fantastic! Will buy again.",
        "Terrible. Waste of money."
    ]
}
df = pd.DataFrame(data)

# Preprocessing function
def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

# Apply preprocessing
df['clean_text'] = df['text'].apply(preprocess)

# Sentiment classification using TextBlob
from textblob import TextBlob

def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

df['sentiment'] = df['clean_text'].apply(get_sentiment)

# Display final output
print(df[['text', 'clean_text', 'sentiment']])
