from django.shortcuts import render
from .models import Post
import nltk
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from .ner import extract_named_entities_with_spacy

# Load the spaCy language model
nlp = spacy.load('en_core_web_sm')

# Create a tokenizer
tokenizer = English().Defaults.create_tokenizer(nlp)

def preprocess_input(text):
    # Tokenize the text
    tokens = tokenizer(text)

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token.text.lower()) for token in tokens]

    # Remove stopwords and punctuation
    tokens = [token for token in tokens if token not in STOP_WORDS and token not in string.punctuation]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def create_post(request):
    if request.method == 'POST':
        # Retrieve user input from the form
        subject = request.POST.get('subject')
        important_things = request.POST.get('important_things')
        libraries = request.POST.get('libraries')
        frameworks = request.POST.get('frameworks')
        tools = request.POST.get('tools')
        best_practices = request.POST.get('best_practices')
        benefits = request.POST.get('benefits')
        examples = request.POST.get('examples')
        implementation_instructions = request.POST.get('implementation_instructions')
        installation_guidelines = request.POST.get('installation_guidelines')
        settings = request.POST.get('settings')
        things_to_avoid = request.POST.get('things_to_avoid')
        top_keywords = request.POST.get('top_keywords')

        # Preprocess the user input
        preprocessed_subject = preprocess_input(subject)

        # Apply spaCy for NER
        named_entities = extract_named_entities_with_spacy(preprocessed_subject)

        # Your remaining code for TF-IDF and keyword extraction can follow here

        # Create a new post object
        post = Post.objects.create(
            subject=subject,
            important_things=important_things,
            libraries=libraries,
            frameworks=frameworks,
            tools=tools,
            best_practices=best_practices,
            benefits=benefits,
            examples=examples,
            implementation_instructions=implementation_instructions,
            installation_guidelines=installation_guidelines,
            settings=settings,
            things_to_avoid=things_to_avoid,
            named_entities=named_entities,
            top_keywords=top_keywords,
        )

        # Render the generated post content to the user
        return render(request, 'post.html', {'post': post})

    return render(request, 'create_post.html')
