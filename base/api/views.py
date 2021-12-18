
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import room
from base.api import serializers


@api_view(['GET'])
def geteoutes(request):
    routes = [
        'GET/api',
        'GET/api/rooms',
        'GET/api/rooms/:id'


    ]
    return Response(routes)


@api_view(['GET'])
def getroom(request):
    rooms = Room.objects.all()
    serializer = room(rooms, many=True)
    return Response(serializer.data)
