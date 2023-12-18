from transformers import BertTokenizer, BertForTokenClassification
import torch

# Load the pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForTokenClassification.from_pretrained(model_name)

# Define the input text for keyword extraction
input_text = "Your input text goes here."

# Tokenize the input text
tokens = tokenizer.tokenize(input_text)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

# Add the special tokens [CLS] and [SEP]
token_ids = [tokenizer.cls_token_id] + token_ids + [tokenizer.sep_token_id]

# Convert the token IDs to tensors
input_ids = torch.tensor([token_ids])

# Run the BERT model for token classification
outputs = model(input_ids)

# Get the predicted token labels
predicted_token_labels = torch.argmax(outputs.logits, dim=2).squeeze().tolist()

# Extract the keywords from the input text
keywords = []
current_keyword = ""
for token, label in zip(tokens, predicted_token_labels[1:-1]):
    if label == 1:  # Check if the token is classified as a keyword
        current_keyword += " " + token
    elif current_keyword:
        keywords.append(current_keyword.strip())
        current_keyword = ""

# Print the extracted keywords
print(keywords)
