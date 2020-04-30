from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

@csrf_exempt
@api_view(["GET"])
def initialize(req):
    user = req.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players}, safe=True)



@api_view(["POST"])
def move(req):
    dirs= {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = req.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(req.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
      
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(req):
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)

@csrf_exempt
@api_view(["GET"])
def rooms(req):
    user = req.user
    player = user.player
    player_id = player.id
    rooms = Room.objects.all()
    return JsonResponse([{
        'room_id': room.id,
        'north': room.n_to != 0,
        'south': room.s_to != 0,
        'east': room.e_to != 0,
        'west': room.w_to != 0,
        'title': room.title,
        'y_coor': room.y,
        'x_coor': room.x,
        'description': room.description,
        'players': room.playerNames(player_id)
    } for  room in rooms], safe=False)