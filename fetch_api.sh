
#!/bin/bash

function cleanup() {

        echo "Cleaning up.."
        rm -rf $tempdir
        rm -rf $tensorflow_dir
        echo "Done."
        exit 0
}

repo="https://github.com/omothm/torch-api"
tempdir="apitemp"
finaldest="torchserver/torchapi"

echo "Fetching API repo..."
mkdir $tempdir
cd $tempdir
error=0

git clone --depth 1 $repo || error=1
cd ..


if [ "$error" == 1 ]; then

        echo "Error cloning. Terminating..."
        cleanup
fi

echo "Removing old repo..."
rm -rf $finaldest

echo "Adding new repo.."
mv -fi $tempdir/torch-api/torchapi $finaldest

tensorflow_dir="models"
if [[ ! -d "${tensorflow_dir}" && ! -L "${tensorflow_dir}" ]] ; then
        echo "Can't find tensorflow files, fetching them"
        git clone --depth 1 https://github.com/tensorflow/models/
fi


pip install cython
pip install pycocotools

cd models
cd research
protoc object_detection/protos/*.proto --python_out=.
pip install .
cd ..
cd ..

cleanup
