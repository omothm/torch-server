from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Banknote
from .serializers import BanknoteSerializer
#from torchapi.api import handle
import json

@api_view(['GET','POST'])
def get_banknote(request):
    if request.method == 'GET':
        # If you're using pylint, you might get a warning that Banknote does not
        # have an 'objects' member. Ignore this warning. Or if you're using VS
        # Code, install pylint-django using pip then add this to the
        # settings.json of the project:
        # "python.linting.pylintArgs": [ "--load-plugins=pylint_django" ]
        banknote = Banknote.objects.all()
        serializer = BanknoteSerializer(banknote, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
            
    elif request.method == 'POST':
        serializer = BanknoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # api_request = { "request":"banknote","image":serializer.data.get('image_base64')}
            # api_response=handle(json.dumps(api_request))
            api_response="TEST"
            return Response(api_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def set_banknote(request,pk):
    try:
        banknote = Banknote.objects.get(pk=pk)
        serializer = BanknoteSerializer(banknote)
    except banknote.DoesNotExist:
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = BanknoteSerializer(banknote)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BanknoteSerializer(banknote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        banknote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        