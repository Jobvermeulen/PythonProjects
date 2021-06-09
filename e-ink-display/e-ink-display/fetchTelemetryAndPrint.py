import io
import os
import sys
import time
import json
import logging
import requests
import traceback
import numpy as np
import epd7in5b_HD
import urllib, base64
from datetime import datetime
import matplotlib.pyplot as plt
from requests.models import Response
from PIL import Image,ImageDraw,ImageFont
from scipy.interpolate import make_interp_spline, BSpline

# Init the pic dir => directory where the pictures are stored
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

# Init the rights fonts => found in the pic dir
robotoFont_18 = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-Regular.ttf'), 18)
robotoFont = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-Regular.ttf'), 32)
robotoFont_bold = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-Bold.ttf'), 32)
robotoFont_bold_h1 = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-Bold.ttf'), 48)
robotoFont_bold_italic = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-BoldItalic.ttf'), 32)
train_one = ImageFont.truetype(os.path.join(picdir, 'fonts/Train_One/TrainOne-Regular.ttf'), 48)

epd = epd7in5b_HD.EPD()

url_telemetry = "http://192.168.1.6:3000/v1/getByDate/"
url_crypto = "https://api.bitvavo.com/v2/ticker/price"

def roomTelemetryFetch(currentDate):    
    formatCurrentDate = currentDate.strftime('%d-%m-%Y')
    response = requests.get(url_telemetry+formatCurrentDate)
    json_response = response.json()
    return json_response

def getCryptoInfo():
    response = requests.get(url_crypto)
    json_response = response.json()
    return json_response

### Main function
### 1. Fetch telemtry data
### 2. (TODO) fetch flower data
### 3. 
def main():
    currentDate = datetime.now();

    # Init screen
    epd.init()

    # Clear out current screen
    epd.Clear()

    time.sleep(20)

    logging.debug("Step 1. Drawing the room temperature on the screen...")

    roomTelemetryImage = Image.new('1', (epd.width, epd.height), 255)
    roomTelemetryImage_red = Image.new('1', (epd.width, epd.height), 255)

    logging.debug("Created image for room telemetry")
    draw_roomTelemetryImage = ImageDraw.Draw(roomTelemetryImage)
    draw_roomTelemetryImage_red = ImageDraw.Draw(roomTelemetryImage_red)
    logging.debug("Drawing image for room telemetry")

    logging.debug('debugging e-ink screen | main function')
    telemetry_json_response = roomTelemetryFetch(currentDate)
    crypto_json_response = getCryptoInfo()
    
    if(len(telemetry_json_response) == 0):
        return;
    
    # Creating graph
    createTempGraph(telemetry_json_response)

    draw_roomTelemetryImage_red.text((15, 5), 'Room Telemetry metrics', font = robotoFont_bold_h1, fill = 0)
    draw_roomTelemetryImage.text((705, 30), currentDate.strftime('%a %d %b. %H:%M'), font = robotoFont_18, fill = 0)
    # FROM => X, Y || TO => X, Y
    draw_roomTelemetryImage.line((15, 65, 850, 65), fill = 0, width=2)

    draw_roomTelemetryImage.text((15, 80), 'Temperature ', font = robotoFont, fill = 0)
    draw_roomTelemetryImage.text((15, 120), 'Humidity ', font = robotoFont, fill = 0)
    draw_roomTelemetryImage.text((230, 80), str(telemetry_json_response[-1]['temp']), font = robotoFont_bold, fill = 0)
    draw_roomTelemetryImage.text((230, 120), str(telemetry_json_response[-1]['humid']), font = robotoFont_bold, fill = 0)
    
    # Crypto currency screen
    if(len(crypto_json_response) != 0):
        cryptoDict = createCryptoDict(crypto_json_response);
        # Draw a rectangle
        draw_roomTelemetryImage.rectangle([(500,80), (850,513)], fill = 0, outline = 0, width = 0)
        draw_roomTelemetryImage.text((592, 95), 'Crypto', font =  train_one, fill = 255)

        # Cardano
        draw_roomTelemetryImage.text((515, 175), 'Cardano', font =  robotoFont, fill = 255)
        draw_roomTelemetryImage.text((710, 175), cryptoDict['ADA-EUR'], font =  robotoFont_bold, fill = 255)

        # NEM
        draw_roomTelemetryImage.text((515, 215), 'Nem', font =  robotoFont, fill = 255)
        draw_roomTelemetryImage.text((710, 215), cryptoDict['XEM-EUR'], font =  robotoFont_bold, fill = 255)

    graph = Image.open(os.path.join(picdir, 'tempGraph.png'))
    roomTelemetryImage_red.paste(graph, (0,160))

    logging.debug("Setting right parameters on image for room telemetry")

    logging.debug('displaying image room telemetry')

    epd.display(epd.getbuffer(roomTelemetryImage), epd.getbuffer(roomTelemetryImage_red))

    time.sleep(20)

    logging.debug('Main function completed...')
    epd.sleep()

def createCryptoDict(crypto_response):
    cryptoListToPrint = ['ADA-EUR', 'XEM-EUR'];
    dict = {}
    for crypto in crypto_response:
        if crypto['market'] in cryptoListToPrint:
            dict[crypto['market']] = crypto['price'];

    return dict

def createTempGraph(json_response):
    temps = np.array([record['temp'] for record in json_response])
    temps = temps.astype(np.float64);
    timestamps = np.array([record['created_on'] for record in json_response])
    plt.figure(figsize=(3,2))

    # 300 represents number of points to make between T.min and T.max
    # xnew = np.linspace(temps.min(), temps.max(), 300) 
    # spl = make_interp_spline(temps,  k=3)  # type: BSpline
    # power_smooth = spl(xnew)

    plt.plot(temps, color= "red", linewidth=4)

    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(True)
   
    plt.yticks(np.arange(min(temps), max(temps) + 1 , step=0.5))        
    plt.tight_layout()

    # plt.figure(figsize=(3,3))
    plt.savefig(os.path.join(picdir, 'tempGraph.png'))


if __name__ == "__main__":
    try:
        # For debugging purposes only!
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('debugging e-ink screen | init function')

        logging.info('starting application!')


        # epd.sleep()

        # # main()
        # # start loop
        while(True):
            main()

            # time.sleep is 30 second -> debug mode
            # time.sleep is 10 minutes -> production mode
            time.sleep(560)
    except:
        logging.exception(traceback.extract_stack)
        epd.sleep()
        logging.error('closing application!')