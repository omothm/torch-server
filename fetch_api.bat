@echo off

set repo=https://github.com/omothm/torch-api
set tempdir=apitemp
set finaldest=torchserver\torchapi

echo Fetching API repo...
mkdir %tempdir%
cd %tempdir%
set error=0
git clone --depth=1 %repo% || set error=1
cd ..

if %error% equ 1 (
	echo Error cloning. Terminating...
	goto cleanup
)

echo Removing old repo...
rmdir /S /Q %finaldest%

echo Adding new repo...
mkdir %finaldest%
move /Y %tempdir%\torch-api\torchapi %finaldest% || set error=1

if %error% equ 1 (
	echo Error in the repo. The repo structure is invalid. Terminating...
	goto cleanup
)

if exist models (
	echo Detected tensorflow model files, no need to pull and compile again.
) else (
	git clone --depth 1 https://github.com/tensorflow/models/
	pip install cython
	pip install pycocotools
	cd models
	cd research
	protoc object_detection/protos/*.proto --python_out=.
	pip install .
	cd ..
	cd ..
)

:cleanup

echo Cleaning up...
rmdir /S /Q %tempdir%

echo Done.
exit /B %error%