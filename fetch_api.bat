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

:cleanup

echo Cleaning up...
rmdir /S /Q %tempdir%

echo Done.
exit /B %error%