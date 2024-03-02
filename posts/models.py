from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    subject = models.CharField(max_length=200)
    important_things = models.TextField(blank=True, null=True)  
    libraries = models.TextField(blank=True,  null=True)
    frameworks = models.TextField(blank=True, null=True)
    tools = models.TextField(blank=True, null=True)
    best_practices = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    examples = models.TextField(blank=True, null=True)
    implementation_instructions = models.TextField(blank=True, null=True)
    installation_guidelines = models.TextField(blank=True, null=True)
    settings = models.TextField(blank=True, null=True)
    things_to_avoid = models.TextField(blank=True, null=True)
    follow = models.TextField(blank=True, null=True)
    hashtags = models.TextField(blank=True, null=True)
    top_keywords = models.TextField(blank=True, null=True)
    textrank_keywords = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.subject

