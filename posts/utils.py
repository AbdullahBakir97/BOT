import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

def preprocess_input(user_input):
    # Tokenize the text into words
    tokens = word_tokenize(user_input)
    
    # Remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]
    
    # Convert to lowercase
    tokens = [token.lower() for token in tokens]
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return lemmatized_tokens