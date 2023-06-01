from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from tasks.serializers import TaskSerializer
from tasks.models import Task
from django.http import JsonResponse, Http404
import requests
import json
from django.http import HttpResponse
from django.conf import settings
import os
import mimetypes

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tasks(request):
    if request.method == 'GET':
        data = Task.objects.all()
        serializer = TaskSerializer(data, many=True)
        return Response({'tasks': serializer.data})
    
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Task' : serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task(request, id):
    try:
        data = Task.objects.get(pk=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TaskSerializer(data)
        return Response({'Task': serializer.data})
    elif request.method == 'DELETE':
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = TaskSerializer(instance=data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Task': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request, id):
    try:
        data = Task.objects.get(pk=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        file = request.FILES['file']
        data.file = file
        data.save()
        return Response({'Task': "File Uploaded Successfully", 'file_path': data.file.url})
    else:
        return Response({'message': 'No file uploaded'})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, id):
    try:
        dataFile = Task.objects.get(pk=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    image_path = os.path.join(settings.MEDIA_ROOT, dataFile.file.name)

    with open(image_path, 'rb') as f:
        response = HttpResponse(f.read())

    response['dataname'] = dataFile.file.name
    response['Content-Type'] = 'application/octet-stream'
    response["Content-Disposition"] = f'attachment; filename="{dataFile.file.name}"'
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)