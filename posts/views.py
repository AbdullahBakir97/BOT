from django.shortcuts import render
from .models import Post
from .forms import PostCreationForm
from .ner import extract_named_entities_with_spacy
from .textrank import extract_keywords_with_textrank
from .tfidf import apply_tfidf
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
import spacy  # Import spacy here

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
        form = PostCreationForm(request.POST)
        if form.is_valid():
            # Cleaned data from the form
            cleaned_data = form.cleaned_data

            # Preprocess the user input
            preprocessed_subject = preprocess_input(cleaned_data['subject'])
            preprocessed_important_things = preprocess_input(cleaned_data['important_things'])

            # Apply spaCy for NER
            named_entities_subject = extract_named_entities_with_spacy(preprocessed_subject)

            # Create a list of preprocessed documents
            preprocessed_documents = [
                preprocessed_subject,
                preprocessed_important_things,
                preprocess_input(cleaned_data['libraries']),
                preprocess_input(cleaned_data['frameworks']),
                preprocess_input(cleaned_data['tools']),
                preprocess_input(cleaned_data['best_practices']),
                preprocess_input(cleaned_data['benefits']),
                preprocess_input(cleaned_data['examples']),
                preprocess_input(cleaned_data['implementation_instructions']),
                preprocess_input(cleaned_data['installation_guidelines']),
                preprocess_input(cleaned_data['settings']),
                preprocess_input(cleaned_data['things_to_avoid']),
                preprocess_input(cleaned_data['top_keywords']),
            ]

            # Apply TextRank for keyword extraction
            textrank_keywords = extract_keywords_with_textrank(preprocessed_subject)

            # Apply TF-IDF vectorization
            tfidf_matrix, feature_names = apply_tfidf(preprocessed_documents)

            # Create a new post object
            post = Post.objects.create(
                subject=preprocessed_subject,
                important_things=preprocessed_important_things,
                libraries=preprocess_input(cleaned_data['libraries']),
                frameworks=preprocess_input(cleaned_data['frameworks']),
                tools=preprocess_input(cleaned_data['tools']),
                best_practices=preprocess_input(cleaned_data['best_practices']),
                benefits=preprocess_input(cleaned_data['benefits']),
                examples=preprocess_input(cleaned_data['examples']),
                implementation_instructions=preprocess_input(cleaned_data['implementation_instructions']),
                installation_guidelines=preprocess_input(cleaned_data['installation_guidelines']),
                settings=preprocess_input(cleaned_data['settings']),
                things_to_avoid=preprocess_input(cleaned_data['things_to_avoid']),
                top_keywords=preprocess_input(cleaned_data['top_keywords']),
                named_entities_subject=named_entities_subject,
                textrank_keywords=textrank_keywords,
            )

            # Render the generated post content to the user
            return render(request, 'post.html', {'post': post, 'tfidf_matrix': tfidf_matrix, 'feature_names': feature_names})

    else:
        form = PostCreationForm()

    return render(request, 'create_post.html', {'form': form})

def generated_post(request):
    # Fetch the most recent post
    latest_post = Post.objects.latest('created_at')

    # Render the 'generated_post.html' template with the post data
    return render(request, 'generated_post.html', {'post': latest_post})