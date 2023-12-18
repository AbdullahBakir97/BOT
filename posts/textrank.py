import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from collections import defaultdict
import string

# Load the spaCy language model
nlp = spacy.load('en_core_web_sm')

# Create a tokenizer
tokenizer = English().Defaults.create_tokenizer(nlp)

def preprocess_input(text):
    # Tokenize the text
    tokens = tokenizer(text)

    # Remove stopwords and punctuation
    tokens = [token.text.lower() for token in tokens if token.text.lower() not in STOP_WORDS and token.text not in string.punctuation]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def extract_keywords_with_textrank(text, num_keywords=5):
    # Preprocess the text
    preprocessed_text = preprocess_input(text)

    # Create a spaCy document
    doc = nlp(preprocessed_text)

    # Build the word frequency dictionary
    word_frequencies = defaultdict(int)
    for token in doc:
        word_frequencies[token.text] += 1

    # Normalize the word frequencies
    max_frequency = max(word_frequencies.values())
    word_frequencies = {word: freq / max_frequency for word, freq in word_frequencies.items()}

    # Calculate the TextRank scores
    tr_scores = defaultdict(float)
    for _ in range(10):  # Number of iterations for convergence
        for token in doc:
            tr_scores[token.text] = (1 - 0.85) + 0.85 * sum(tr_scores[t.text] * word_frequencies[t.text] for t in token.children)

    # Sort the keywords by TextRank scores
    keywords = sorted(tr_scores, key=tr_scores.get, reverse=True)[:num_keywords]

    return keywords