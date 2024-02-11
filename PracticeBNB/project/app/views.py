from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Event, Registration
from .forms import RegistrationForm
from .forms import EventForm, OrganizerLoginForm
from django.contrib import messages
from .forms import RaisedHandForm
from .models import RaisedHand, Comment
from django.db.models import Count
from .forms import CommentForm


def comment_page(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            # Redirect to the same page to display the updated comment list
            return redirect('comment_page')
    else:
        form = CommentForm()

    comments = Comment.objects.all()  # Retrieve all comments
    return render(request, 'comment_page.html', {'form': form, 'comments': comments})


def leaderboard(request):
    # Get a list of users with their respective registration counts
    user_registration_counts = Registration.objects.values('user').annotate(
        registration_count=Count('user')).order_by('-registration_count')

    # Get user objects and their registration counts
    leaderboard_data = [{'user': User.objects.get(
        pk=item['user']), 'registration_count': item['registration_count']} for item in user_registration_counts]

    return render(request, 'leaderboard.html', {'leaderboard_data': leaderboard_data})


def recent_events(request):
    events = Event.objects.all()
    return render(request, 'recent_events.html', {'events': events})


def register_for_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user  # Assuming user is logged in
            registration.event = event
            registration.save()
            return redirect('success_page')
    else:
        form = RegistrationForm()
    return render(request, 'registration_form.html', {'form': form, 'event': event})


def success_page(request):
    # Get the logged-in user
    user = request.user

    # Count the number of registrations for the logged-in user
    registration_count = Registration.objects.filter(user=user).count()

    return render(request, 'success_page.html', {'registration_count': registration_count})


def raise_hand(request):
    if request.method == 'POST':
        form = RaisedHandForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            interests = form.cleaned_data['interests']
            RaisedHand.objects.create(name=name, interests=interests)
            return redirect('raised_hands')
    else:
        form = RaisedHandForm()
    return render(request, 'raise_hand.html', {'form': form})


def raised_hands(request):
    raised_hands = RaisedHand.objects.all()
    return render(request, 'raised_hands.html', {'raised_hands': raised_hands})


@login_required
def calendar(request):
    events = Event.objects.all()
    return render(request, 'calendar.html', {'events': events})


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            # Redirect to the calendar after adding the event
            return redirect('recent_events')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


@login_required
def edit_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.organizer:
        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('calendar')
        else:
            form = EventForm(instance=event)
        return render(request, 'edit_event.html', {'form': form})
    else:
        return redirect('calendar')


@login_required
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.organizer:
        event.delete()
    return redirect('calendar')


def show_interest(request, event_id):
    # Implement logic to track user interest in the event
    return redirect('calendar')


def add_event_login(request):
    if request.method == 'POST':
        form = OrganizerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.groups.filter(name='Event Organizers').exists():
                    login(request, user)
                    return redirect('calendar')
        else:
            messages.error(
                request, 'Invalid username or password. Please try again.')
    else:
        form = OrganizerLoginForm()
    return render(request, 'add_event_login.html', {'form': form})


def index(request):
    return render(request, 'welcome.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirect to the home page after successful login
            return render(request, 'home.html')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('login')
