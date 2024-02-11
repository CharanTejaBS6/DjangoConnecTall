from django import forms
from .models import Event
from .models import Registration, Comment

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['email', 'phone_number', 'payment_info']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date']


class OrganizerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RaisedHandForm(forms.Form):
    name = forms.CharField(max_length=100)
    interests = forms.CharField(widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }