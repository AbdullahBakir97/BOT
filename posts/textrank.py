import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
from collections import defaultdict

# Load the spaCy English language model
nlp = spacy.load('en_core_web_sm')

def preprocess_input(text):
    # Tokenize the text using spaCy's built-in tokenizer
    tokens = nlp.tokenizer(text)

    # Remove stopwords and punctuation from tokens
    tokens = [
        token.text.lower() for token in tokens 
        if not token.is_stop and not token.is_punct
    ]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def extract_keywords_with_textrank(text, num_keywords=5):
    # Preprocess the text
    preprocessed_text = preprocess_input(text)

    # Create a spaCy document from the preprocessed text
    doc = nlp(preprocessed_text)

    # Build the word frequency dictionary
    word_frequencies = defaultdict(int)
    for token in doc:
        if not token.is_stop and not token.is_punct:
            word_frequencies[token.text] += 1

    # Normalize the word frequencies
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency

    # Calculate the TextRank scores
    tr_scores = defaultdict(float)
    for token in doc:
        for child in token.children:
            tr_scores[token.text] += word_frequencies[child.text]

    for _ in range(10):  # Number of iterations for convergence
        for token in doc:
            tr_scores[token.text] = (1 - 0.85) + 0.85 * sum(tr_scores[child.text] for child in token.children)

    # Sort the keywords by TextRank scores
    keywords = sorted(tr_scores, key=tr_scores.get, reverse=True)[:num_keywords]

    return keywords

# Example usage
if __name__ == "__main__":
    sample_text = "Natural language processing enables computers to understand human language. It's a field of artificial intelligence."
    print(extract_keywords_with_textrank(sample_text))