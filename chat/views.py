from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm
from accounts.models import DoctorProfile, PatientProfile
from django.db import models

# Create your views here.

@login_required
def chat_list(request):
    # Show all users the current user has chatted with
    user = request.user
    sent_to = Message.objects.filter(sender=user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=user).values_list('sender', flat=True)
    user_ids = set(list(sent_to) + list(received_from))
    users = User.objects.filter(id__in=user_ids).exclude(id=user.id)
    return render(request, 'chat/chat_list.html', {'users': users})

@login_required
def chat_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    user = request.user
    # Get all messages between the two users
    messages = Message.objects.filter(
        (models.Q(sender=user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=user))
    ).order_by('timestamp')
    # Mark received messages as read
    messages.filter(receiver=user, is_read=False).update(is_read=True)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = user
            msg.receiver = other_user
            msg.save()
            return redirect('chat_detail', user_id=other_user.id)
    else:
        form = MessageForm()
    return render(request, 'chat/chat_detail.html', {
        'messages': messages,
        'form': form,
        'other_user': other_user,
    })

@login_required
def start_chat(request):
    # For patients: list doctors; for doctors: list patients
    user = request.user
    if hasattr(user, 'patientprofile'):
        doctors = DoctorProfile.objects.filter(is_approved=True)
        return render(request, 'chat/start_chat.html', {'users': [doc.user for doc in doctors]})
    elif hasattr(user, 'doctorprofile'):
        patients = PatientProfile.objects.all()
        return render(request, 'chat/start_chat.html', {'users': [pat.user for pat in patients]})
    else:
        return redirect('chat_list')
