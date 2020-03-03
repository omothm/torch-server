from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Banknote
from .serializers import BanknoteSerializer
from django.http import HttpResponse
from torchapi.api import handle
import json
import base64

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
                    The value for image must contain a URL safe base64 encoded string! 
                    (no metatag) --> (data:image/jpeg;base64,)
                    This string will be then converted into normal base64 because that is what API expects.


        HTTP response will be in JSON format.
        E.g.
            {
                "status": "ok",
                "time": "2020-02-25 19:50:53.833346",
                "response": 100
            }
        """


        """
            ### IMPORTANT ###
            Don't expect the metatag for the base64 encoded image
            (The ';' char is a reserved character for the URLs so should not be used.)
            As a temporary solution just ask for the base64 URL encoded string and append the 
            metadata manually before calling the handle function.     
        """

        # Get the passed in parameters 'service' and 'image'
        requested_service = request.GET.get('service', '')
        base64_encoded_image = request.GET.get('image', '')
        # Check if the service parameter is provided
        if requested_service == '':
            error_response = {}
            error_response["status"] = "error"
            error_response["error_origin"] = "client"
            error_response["error_message"] = "Please provide a valid value for 'service' parameter."
            return HttpResponse(json.dumps(error_response))
        try:
            #convert the image to normal base64 from URL safe base64
            decoded_data = base64.urlsafe_b64decode(base64_encoded_image.encode('utf-8')) # bytes
            #Now convert to normal base64 (This is what api expects!)
            base64_encoded_str = str(base64.b64encode(decoded_data),'utf-8')
            #Append a dummy metatag, this is what API expects.
            base64_encoded_str = "data:image/jpeg;base64," + base64_encoded_str
            #prepare the request as JSON (for Torch API)
            api_req = {}
            api_req['request'] = requested_service
            api_req['image'] = base64_encoded_str
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
            Currently not expecting POST requests, but may be implemented
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
        error_response = {}
        error_response["status"] = "error"
        error_response["error_origin"] = "torch server"
        error_response["error_message"] = "Please use GET method to access Torch API."
        return HttpResponse(json.dumps(error_response))

    else:
        error_response = {}
        error_response["status"] = "error"
        error_response["error_origin"] = "torch server"
        error_response["error_message"] = request.method + " is not supported.Please use GET method to access Torch API."
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