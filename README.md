# Torch Server

## Running

Either:
- Run the batch file `run.bat`, or
- Run it manually:
	
	```
	cd torchserver
	
  python manage.py runserver
	```

## Fetching the API

The API is hosted in another repository. To fetch and place the API here, you may do **ONE** of the following:

- Run `run.bat` with `-f` or `--fetch` flag.
- Run `fetch_api.bat`.
- Do it manually:
	
	```
  mkdir temp && cd temp
  
	git clone https://github.com/omothm/torch-api
	
	move /Y temp\torch-api\torchapi torchserver\torchapi
	
	rmdir /S temp
	```
