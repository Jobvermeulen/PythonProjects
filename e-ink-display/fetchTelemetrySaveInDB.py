import time
import smbus
import board
import logging
import requests
import traceback
import statistics
import adafruit_dht
from datetime import datetime

# Init the temp and humidity sensor
# DHT22 -> The newer and a more precisely sensor
# DHT11 -> the older and a less precisely sensor
telemetrySensor = adafruit_dht.DHT22(21)

# Init base url
baseUrl = "http://192.168.1.6:3000/v1"

# Main function
# Step 1. Read telemetrics 
# -> Three times, each time there is a three second delay
# -> Once finished the median of the results is calculated
# Step 2. Save the median of the telemetrics to the database
# -> Localted on localhost POST method (192.168.1.6/v1/telemetrics)
def main():
    logging.debug('Starting main function')

    # Define current time 
    timeStamp = datetime.now()
    timeStampFormat = timeStamp.strftime("%d/%m/%Y, %H:%M")
    
    logging.debug("timestamp: " + str(timeStampFormat))

    # Define itterator
    i = 0

    # Define array's telemetry
    tempArray = []
    humidArray = []

    # While functions are less memory intensive 
    # While functions are less cpu intensive
    while(i < 3):
        tempArray.append(telemetrySensor.temperature)
        humidArray.append(telemetrySensor.humidity)
        logging.debug(tempArray[i])
        logging.debug(humidArray[i])
        
        i = i + 1
        time.sleep(3)

    # Calculate medians
    tempMedian = statistics.median(tempArray)
    humidMedian = statistics.median(humidArray)
    logging.debug("Temp median: " + str(tempMedian) + "\n Humid median: " + str(humidMedian))
    
    # Save to database
    requests.post(baseUrl+'/telemetry', {"temp": tempMedian, "humid": humidMedian, "created_on": timeStampFormat})
    
if __name__ == "__main__" :
    try: 
        logging.basicConfig(level=logging.DEBUG)
        main()
    except:
        logging.exception(traceback.extract_stack)
        logging.info('closing application')
