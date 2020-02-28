from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Banknote
from .serializers import BanknoteSerializer
from django.http import HttpResponse
#from torchapi.api import handle
import json

@api_view(['GET','POST'])
def api_get_request(request):
    if request.method == 'GET':
        """
        GET HTTP request for '{domain}/api/'
        Expects a parameter on the URL named 'query', it should contaion a JSON
        E.g.
            HTTP GET 
            {domain}/api/?query=
                {
                    "requested_service":"banknote_detection",
                    "b64_encoded_image":"ABCabc123"
                }

        HTTP response will be in JSON format.
        E.g.
            {
                "status": "ok",
                "time": "2020-02-25 19:50:53.833346",
                "response": 100
            }
        """
        request_parameters = request.GET.get('query', '')
        request_parameters_json = json.loads(request_parameters)

        # Send the query to Torch API and return the output to the client HERE.
        
        # Place holder response.
        return HttpResponse("You have requested (" + str(request_parameters_json['request_service']) + ") service!")
            
    elif request.method == 'POST':
        """
            Currently not expecting POST requests, but maybe implemented
            in the future for receiving binary image files.
        """

        """
        serializer = BanknoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # api_request = { "request":"banknote","image":serializer.data.get('image_base64')}
            # api_response=handle(json.dumps(api_request))
            api_response="TEST"
            return Response(api_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """
        
        return HttpResponse("Please use GET method to access Torch API.")


"""
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
        
"""