# JSON API for Raspberry providing information about status. #

## Features ##
- get CPU temperature
- get CPU speed
- get System temperature
- get temperature of attached DHT22 sensor


## Needed python libraries (install with pip install) ##
- Flask (for the json remote API)
- Adafruit_DHT (download from https://github.com/adafruit/Adafruit_Python_DHT)


## Info ##
Query like REST API example "http://raspberrypi:5005/v1.0/query/cpu_temp".
DHT 22 connected to GPIO24