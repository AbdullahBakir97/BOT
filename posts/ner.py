import spacy
from spacy.lang.en import English

def extract_named_entities_with_spacy(text):
    nlp = spacy.load('en_core_web_sm')
    tokenizer = English().Defaults.create_tokenizer(nlp)
    
    # Tokenize the text
    tokens = tokenizer(text)
    
    # Create a spaCy document
    doc = spacy.tokens.Doc(nlp.vocab, words=[token.text for token in tokens])
    
    # Apply named entity recognition
    nlp.get_pipe("ner")(doc)
    
    # Extract named entities
    named_entities = [ent.text for ent in doc.ents]
    
    return named_entities