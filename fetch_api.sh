
#!/bin/bash

function cleanup() {

echo "Cleaning up.."
rm -rf $tempdir
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

git clone $repo || error=1
cd ..


if [ "$error" == 1 ]; then

        echo "Error cloning. Terminating..."
        cleanup
fi

echo "Removing old repo..."
rm -rf $finaldest

echo "Adding new repo.."
mv -fi $tempdir/torch-api/torchapi $finaldest

cleanup
