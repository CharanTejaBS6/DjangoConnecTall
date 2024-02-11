from django.db import models
from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(default=timezone.now)  # Default value set to current date/time
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Assuming user ID 1 exists

    def __str__(self):
        return self.title

class Reminder(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    reminder_date = models.DateField()


class OrganizerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Check if the provided username and password match the fixed values
        if username != 'Cherry' or password != 'Tej':
            raise forms.ValidationError("Invalid username or password")

        return cleaned_data
    

class RaisedHand(models.Model):
    name = models.CharField(max_length=100)
    interests = models.TextField()

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    payment_info = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Badge(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='badges')
    name = models.CharField(max_length=100)