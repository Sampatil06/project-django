import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import Message
from django.db.models import Q

def landing_page(request):
    return render(request, 'landing.html')

def signup(request):
    """
    Handles user signup.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('chat')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def chat(request):
    """
    Displays the chat interface with a list of users.
    """
    users = User.objects.exclude(id=request.user.id) 
    return render(request, 'chat.html', {'users': users})



@login_required
def get_messages(request, recipient_id):
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient_id=recipient_id)) |
        (Q(sender_id=recipient_id) & Q(recipient=request.user))
    ).order_by('timestamp')

    data = [{'sender': message.sender.username, 'content': message.content} for message in messages]
    return JsonResponse(data, safe=False)