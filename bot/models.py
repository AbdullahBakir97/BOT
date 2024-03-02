from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup


class Bot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='active')
    created_at = models.DateTimeField(default=timezone.now)
    integration_service = models.CharField(max_length=100, blank=True)
    integration_credentials = models.CharField(max_length=100, blank=True)
    log = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def generate_post(self, subject):
        """
        Method to generate a post based on the subject using BERT model.
        
        Parameters:
            subject (str): The subject of the post.
        
        Returns:
            Post: The generated post object.
        """
        # Load pre-trained BERT model and tokenizer
        model_name = 'bert-base-uncased'
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertForSequenceClassification.from_pretrained(model_name)

        # Prepare input text for BERT
        input_text = f"Subject: {subject}"
        input_ids = tokenizer.encode(input_text, add_special_tokens=True, return_tensors='pt')

        # Generate post content using BERT
        outputs = model(input_ids)
        predicted_label = torch.argmax(outputs.logits).item()

        if predicted_label == 0:
            # Negative class: generate negative post content
            generated_content = "This is a negative post."
        else:
            # Positive class: generate positive post content
            generated_content = "This is a positive post."

        # Create a new post associated with this bot
        post = Post.objects.create(
            subject=subject,
            content=generated_content,
            user=self.owner
        )

        return post

    def search_internet(self, query, post):
        """
        Method to search the internet based on a query.
        
        Parameters:
            query (str): The search query.
        
        Returns:
            list: List of URLs retrieved from the search.
        """
        search_url = f"https://www.google.com/search?q={query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                search_results = []
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href.startswith('/url?q='):
                        url = href.replace('/url?q=', '').split('&')[0]
                        search_results.append(url)
                
                # Assuming you have a Post instance named 'post'
                query = query  # You can use the subject of the post as the search query
                post.search_results = search_results
                post.save()
                
                return search_results
            else:
                return None
        except Exception as e:
            # Log the error or handle it accordingly
            print(f"Error occurred while searching: {e}")
            return None

    def interact_with_user(self, message):
        """
        Method to interact with users based on their message.
        
        Parameters:
            message (str): The message from the user.
        
        Returns:
            str: The response to be sent back to the user.
        """
        # Define some predefined responses based on user input
        predefined_responses = {
            "hello": "Hello! How can I assist you today?",
            "how are you": "I'm just a bot, but thanks for asking!",
            "goodbye": "Goodbye! Have a great day!"
        }

        # Convert the user's message to lowercase for case-insensitive matching
        message = message.lower()

        # Check if the bot has a predefined response for the user's message
        if message in predefined_responses:
            return predefined_responses[message]
        else:
            # If no predefined response, provide a generic response
            return "I'm sorry, I didn't understand your message. How can I assist you?"

    def log_event(self, event):
        """
        Method to log events.
        
        Parameters:
            event (str): The event to be logged.
        """
        log_entry = f"{timezone.now()}: {event}"
        self.log += f"\n{log_entry}"
        self.save()


