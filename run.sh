#!/bin/bash

fetch=0
if [ "$1" == "-f" ] || [ "$1" == "--fetch" ] ; then
        fetch=1
fi
fetcherror=0

if [ "$fetch" == 1 ] ; then
        echo "Fetching the latest version of the API..."
        ./fetch_api.sh || fetcherror=1
        if [ "$fetcherror" == 1 ] ; then
                echo "Error ocurred in fetching. Terminating..."
                exit 0
        fi
else
        echo "INFO: Running on the existing API [may not be up-to-date]"
fi

echo "Running server..."
cd torchserver
python manage.py runserver 0.0.0.0:8000
cd ..

exit 0
