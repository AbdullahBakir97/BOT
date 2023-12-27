# forms.py
from django import forms
from .models import Post

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'important_things', 'libraries', 'frameworks', 'tools', 'best_practices', 'benefits', 'examples', 'implementation_instructions', 'installation_guidelines', 'settings', 'things_to_avoid', 'top_keywords']
