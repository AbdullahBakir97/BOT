from django.db import models


class Post(models.Model):
    subject = models.CharField(max_length=200)
    important_things = models.TextField(null=True,blank=True)
    libraries = models.TextField(null=True,blank=True)
    frameworks = models.TextField(null=True,blank=True)
    tools = models.TextField(null=True,blank=True)
    best_practices = models.TextField(null=True,blank=True)
    benefits = models.TextField(null=True,blank=True)
    examples = models.TextField(null=True,blank=True)
    implementation_instructions = models.TextField(null=True,blank=True)
    installation_guidelines = models.TextField(null=True,blank=True)
    settings = models.TextField(null=True,blank=True)
    things_to_avoid = models.TextField(null=True,blank=True)
    follow = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.TextField(null=True,blank=True)
    top_keywords = models.TextField(null=True,blank=True)

    def _str_(self):
        return self.subject