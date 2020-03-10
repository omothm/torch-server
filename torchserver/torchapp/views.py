import json
import urllib.parse

from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse

import torchapi


@api_view(['GET', 'POST'])
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
        base64_encoded_image = urllib.parse.unquote_plus(
            request.GET.get('image', ''))  # decode the image parameter

    elif request.method == 'POST':
        """
            POST request expects the 'service' parameter from the url,
            but the base64 encoded image is expected from the body of the request
        """
        # get the body of the request (image)
        base64_encoded_image = request.body.decode('utf-8')

    else:
        msg = request.method + \
            " is not supported. Please use GET or POST method to access Torch API."
        response = torchapi.error_response(origin="server", msg=msg)
        return JsonResponse(response)

    # Get the passed in parameters 'service'
    requested_service = request.GET.get('service')

    try:
        # prepare the request as JSON (for Torch API)
        api_req = {
            "request": requested_service,
            "image": base64_encoded_image
        }
        api_req_str = json.dumps(api_req)
    except Exception as err:
        # An exception happened during the convertion and preperation of JSON
        response = torchapi.error_response(origin="server", msg=str(err))
        return JsonResponse(response)

    try:
        # Send the query to Torch API and return the output to the client HERE.
        response = torchapi.handle(api_req_str)
        return HttpResponse(response)
    except Exception as err:
        response = torchapi.error_response(origin="api", msg=str(err))
        return JsonResponse(response)
