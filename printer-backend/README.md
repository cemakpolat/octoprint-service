
Install Dependencies

`python setup.py install`

or 

`pip install -r requirements.txt`

or 

`./service.sh install `

Start printer-backend

`python src/main.py`

or 

`./service.sh start`

Stop service

`./service.sh stop`




"""
    1. get all port numbers from docker-interface
    2. call the java api for each port to see whether the printer is running or not
    3. create a list of available printers
    4. choose randomly one of the printers
    5. future task: based on the printer features, take different decisions.
"""