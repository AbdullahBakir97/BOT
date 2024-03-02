from django import forms
from .models import Post

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'important_things', 'libraries', 'frameworks', 'tools', 'best_practices', 'benefits', 'examples', 'settings', 'things_to_avoid']
        widgets = {
            'important_things': forms.Textarea,
            'libraries': forms.Textarea,
            'frameworks': forms.Textarea,
            'tools': forms.Textarea,
            'best_practices': forms.Textarea,
            'benefits': forms.Textarea,
            'examples': forms.Textarea,
            'settings': forms.Textarea,
            'things_to_avoid': forms.Textarea,
        }
        
    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        # Add custom validation or cleaning for the subject field if needed
        return subject

    def clean_important_things(self):
        important_things = self.cleaned_data.get('important_things')
        # Add custom validation or cleaning for the important_things field if needed
        return important_things

    # Define clean methods for other fields as needed

    def save(self, commit=True):
        # Override the save method to add custom logic if needed
        post = super().save(commit=False)
        # Add any additional processing before saving the post object
        if commit:
            post.save()
        return post