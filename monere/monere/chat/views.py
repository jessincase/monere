import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from django.template.loader import render_to_string
from django.http import JsonResponse
from haikunator import Haikunator
from .models import Room
import jsonpickle


def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            haikunator = Haikunator()
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label, poster = request.user)

    return JsonResponse({'label' : label })

@login_required
def chat_room(request, label):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    room = get_object_or_404(Room,label=label)
    messages = reversed(room.messages.order_by('-timestamp'))

    room_json = jsonpickle.encode(room)
    messages_json = jsonpickle.encode(messages)

    return JsonResponse({
        'room': room_json,
        'messages': messages_json
    })


@login_required
def popup_chatroom(request, label):
    room = get_object_or_404(Room, label=label)
    messages = reversed(room.messages.order_by('-timestamp'))
    room_json = jsonpickle.encode(room)
    messages_json = jsonpickle.encode(messages)

    return JsonResponse({'room': room_json, 'messages': messages_json})

@login_required
def user_rooms_sidebar(request):
    rooms = Room.objects.filter(poster=request.user)
    room_count = len(rooms)
    rooms_json = jsonpickle.encode(rooms)

    return JsonResponse({ 'rooms': rooms_json, 'room_count': room_count})

@login_required
def save_room(request, label):
    room = get_object_or_404(Room, label=label)
    user = request.user
    user.saved_rooms.add(room)
    user.save()

    return JsonResponse({'result' : True })
