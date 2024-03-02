import spacy

# Load the spaCy language model
nlp = spacy.load('en_core_web_sm')

def extract_named_entities_with_spacy(text):
    # Create a spaCy document that also runs the NER pipeline component
    doc = nlp(text)
    
    # Extract named entities
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    return named_entities

# Example usage
if __name__ == "__main__":
    sample_text = "Apple is looking at buying U.K. startup for $1 billion"
    print(extract_named_entities_with_spacy(sample_text))