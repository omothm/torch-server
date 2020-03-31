import json
import urllib.parse

from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse

import torchapi

import os
import random

_POPULATION = list(map(chr, list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))))
_RANDOM_STRING_LENGTH = 32

@api_view(['GET', 'POST'])
def api_request_handler(request):
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


        # Save this image to the disk to increase the dataset population
        current_path = os.path.dirname(os.path.realpath(__file__))

        # Convert the base64 image to binary image file and save it
        try:
            binary_image = torchapi.services.common.base64_to_image_obj(api_req)

            # Get the unlabeled directory path
            unlabeled_dir = os.path.join(os.path.abspath(
                os.path.join(
                    os.path.join(
                        current_path, os.pardir), os.pardir)),'inference_results','not_labeled')

            # Check if the directory exists, create otherwise        
            if not os.path.exists(unlabeled_dir):
                os.makedirs(unlabeled_dir)

            # Generate the name of the file
            dict_response = json.loads(response)

            random_file_name = requested_service + '_' + str(dict_response['response']) + '_' + get_random_name() + '.jpg'

            
            with open(os.path.join(unlabeled_dir,random_file_name), 'wb') as current_image_file:
                current_image_file.write(binary_image)

            # Append the filename to response, so that user can confirm the accuracy later
            dict_response['saved_file_name'] = random_file_name
            response = json.dumps(dict_response)
        except Exception as err:
            print(err)


        return HttpResponse(response)
    except Exception as err:
        response = torchapi.error_response(origin="api", msg=str(err))
        return JsonResponse(response)


@api_view(['GET', 'POST'])
def api_contribute_request_handler(request):

    """
        GET or POST http request for '{domain}/api/contribute/'
        Expects 2 parameters from the URL named 'image_file_name' and 'is_correct_classification'
        E.g.
            HTTP GET 
            {domain}/api/
                ?image_file_name=banknote_20_16QXW0dVsiYP2UywIlwvq9Ud8VtVdfuv.jpg
                &is_correct_classification=true

        If the classification is true, the saved image file will be moved to another
        directory that consists of only approved image files with the same labeled class.
    """

    if request.method == 'GET' or request.method == "POST":
        # Get the image_file name
        image_file_name = request.GET.get('image_file_name', '')

        if image_file_name == "":
            error_response = {}
            error_response['status'] = 'Error'
            error_response['response'] = 'Please provide the "image_file_name" parameter on the request url.'
            return HttpResponse(json.dumps(error_response))


        # Get the result of classification
        is_correct_classification = request.GET.get('is_correct_classification', 'False')
        is_correct_classification = (is_correct_classification == True) or (is_correct_classification == "True") or (is_correct_classification == "true")

        if is_correct_classification :
            # Now move this image to new valid directory

            # Check if the image exists
            current_path = os.path.dirname(os.path.realpath(__file__))
            inference_results_dir = os.path.join(
                os.path.abspath(os.path.join(
                    os.path.join(
                        current_path, os.pardir), os.pardir)),'inference_results')

            image_path = os.path.join(inference_results_dir,'not_labeled',image_file_name)

            if os.path.isfile(image_path) and os.access(image_path, os.R_OK):
                # Image file exists, copy the image file to the approved directory
                approved_target_directory = os.path.join(
                    inference_results_dir,'approved_' + 
                        image_file_name.split('_')[0] + '_' + image_file_name.split('_')[1])

                # Check if directory exitst, create otherwise
                if not os.path.exists(approved_target_directory):
                    os.makedirs(approved_target_directory)

                final_image_destination = os.path.join(approved_target_directory,image_file_name)

                # Now move the image to approved folder
                os.replace(image_path,final_image_destination)
            

    response = {}
    response['status'] = 'ok'
    response['response'] = 'Thanks for your contribution.'
    return HttpResponse(json.dumps(response))


def get_random_name() -> str:
    return "".join(random.choices(_POPULATION, k=_RANDOM_STRING_LENGTH))