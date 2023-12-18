from sklearn.feature_extraction.text import TfidfVectorizer

def apply_tfidf(corpus):
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=500,  # Limit the number of features (terms)
        stop_words='english',  # Remove common English stopwords
        lowercase=True,  # Convert all text to lowercase
        use_idf=True,  # Include IDF (Inverse Document Frequency) in the calculation
        smooth_idf=True,  # Smooth IDF weights to prevent division by zero
        sublinear_tf=True  # Apply sublinear TF scaling
    )
    
    # Apply TF-IDF vectorization to the corpus
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Get the feature names (terms)
    feature_names = vectorizer.get_feature_names()
    
    return tfidf_matrix, feature_names