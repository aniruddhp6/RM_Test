from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from apiapp.serializers import ItemSerializer, ItemGetAllSerializer
from rest_framework.response import Response
from .models import Item
from marshmallow import ValidationError
import requests
import time
import concurrent.futures


@api_view(['POST'])
def add_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        a = serializer.validated_data['item']
        list1 = ["book", "pen", "folder", "bag"]
        if a in list1:
            serializer.save()
            items = Item.objects.all().order_by('-id')[0]
            return Response({"Status": "Added", "Recently Inserted Item": {"id": items.id, "status": items.status, "item": items.item}}, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError("Wrong Item Inserted")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
def get_all_items(request):
    items = Item.objects.all().order_by('-item')
    serializer = ItemGetAllSerializer(items, many=True)
    return Response(serializer.data)


@ api_view(['GET'])
def search_item(request):
    value = request.GET['delay_value']
    delay_value = [value] * 5
    start = time.time()

    def work(delay_value):
        r = requests.get(
            'https://httpbin.org/delay/{delay_value}'.format(delay_value=delay_value)).json()
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(work, delay_value)
    request_time = time.time() - start
    return Response({"Time Taken": request_time}, status=status.HTTP_200_OK)
