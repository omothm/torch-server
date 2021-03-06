@echo off

set fetch=0
if "%1" == "-f" set fetch=1
if "%1" == "--fetch" set fetch=1
if %fetch% equ 1 (
	echo Fetching the latest version of the API...
	call fetch_api || (
		echo Error ocurred in fetching. Terminating...
		goto terminate
	)
) else (
	echo INFO: Running on the existing API [may not be up-to-date]
)

echo Running server...
cd torchserver
python manage.py runserver
cd ..

:terminate