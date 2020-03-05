from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Banknote
from .serializers import BanknoteSerializer
from django.http import HttpResponse
from torchapi.api import handle
import json
import base64
import urllib.parse

@api_view(['GET','POST'])
def api_get_request(request):
    if request.method == 'GET':
        """
        GET HTTP request for '{domain}/api/'
        Expects 2 parameter on the URL named 'service' and 'image', 
        E.g.
            HTTP GET 
            {domain}/api/
                ?service=banknote
                &image=ABCabc123


                ### IMPORTANT ###
                    The value for image must contain base64 encoded string
                    This string should start with a metatag --> (data:image/jpeg;base64,)


        HTTP response will be in JSON format.
        E.g.
            {
                "status": "ok",
                "time": "2020-02-25 19:50:53.833346",
                "response": 100
            }
        """

        # Get the passed in parameters 'service' and 'image'
        requested_service = request.GET.get('service', '')
        base64_encoded_image = urllib.parse.unquote_plus(request.GET.get('image', '')) # decode the image parameter

        # Check if the service parameter is provided
        if requested_service == '':
            error_response = {}
            error_response["status"] = "error"
            error_response["error_origin"] = "client"
            error_response["error_message"] = "Please provide a valid value for 'service' parameter."
            return HttpResponse(json.dumps(error_response))
        try:
            #prepare the request as JSON (for Torch API)
            api_req = {}
            api_req['request'] = requested_service
            api_req['image'] = base64_encoded_image
            api_req_str = json.dumps(api_req)
        except Exception as err:
            #An exception happened during the convertion and preperation of JSON
            error_response = {}
            error_response["status"] = "error"
            error_response["error_origin"] = "torch server"
            error_response["error_message"] = str(err)
            return HttpResponse(json.dumps(error_response))
            
        try:
            # Send the query to Torch API and return the output to the client HERE.
            response = handle(api_req_str)
            return HttpResponse(json.dumps(response))
        except Exception as err:
            error_response = {}
            error_response["status"] = "error"
            error_response["error_origin"] = "torch API"
            error_response["error_message"] = str(err)
            return HttpResponse(json.dumps(error_response))


            
    elif request.method == 'POST':
        """
            POST request expects the 'service' parameter from the url,
            but the base64 encoded image is expected from the body of the request
        """
        

        # Get the passed in parameters 'service'
        requested_service = request.GET.get('service', '')

        # get the body of the request (image)
        base64_encoded_image = request.body.decode('utf-8')

        # Check if the service parameter is provided
        if requested_service == '':
            error_response = {}
            error_response["status"] = "error"
            error_response["error_origin"] = "client"
            error_response["error_message"] = "Please provide a valid value for 'service' parameter."
            return HttpResponse(json.dumps(error_response))
        try:
            #prepare the request as JSON (for Torch API)
            api_req = {}
            api_req['request'] = requested_service
            api_req['image'] = base64_encoded_image
            api_req_str = json.dumps(api_req)
        except Exception as err:
            #An exception happened during the convertion and preperation of JSON
            error_response = {}
            error_response["status"] = "error"
            error_response["error_origin"] = "torch server"
            error_response["error_message"] = str(err)
            return HttpResponse(json.dumps(error_response))
            
        try:
            # Send the query to Torch API and return the output to the client HERE.
            response = handle(api_req_str)
            return HttpResponse(json.dumps(response))
        except Exception as err:
            error_response = {}
            error_response["status"] = "error"
            error_response["error_origin"] = "torch API"
            error_response["error_message"] = str(err)
            return HttpResponse(json.dumps(error_response))


    else:
        error_response = {}
        error_response["status"] = "error"
        error_response["error_origin"] = "torch server"
        error_response["error_message"] = request.method + " is not supported.Please use GET or POST method to access Torch API."
        return HttpResponse(json.dumps(error_response))


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