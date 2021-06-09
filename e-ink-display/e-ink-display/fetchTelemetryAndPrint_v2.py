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

class fetchTelemetry:
    # URLs
    url_telemetry = "http://192.168.1.6:3000/v1/getByDate/"
    url_crypto = "https://api.bitvavo.com/v2/ticker/price"

    # PicDir
    picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

    # Fonts
    robotoFont_18 = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-Regular.ttf'), 18)
    robotoFont = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-Regular.ttf'), 32)
    robotoFont_bold = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-Bold.ttf'), 32)
    robotoFont_bold_h1 = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-Bold.ttf'), 48)
    robotoFont_bold_italic = ImageFont.truetype(os.path.join(picdir, 'fonts/Roboto/Roboto-BoldItalic.ttf'), 32)
    train_one = ImageFont.truetype(os.path.join(picdir, 'fonts/Train_One/TrainOne-Regular.ttf'), 48)

    # Init epd
    epd = epd7in5b_HD.EPD()

    # Images
    Image_black = Image.new('1', (epd.width, epd.height), 255)
    Image_red = Image.new('1', (epd.width, epd.height), 255)
    draw_Image = ImageDraw.Draw(Image_black)
    draw_Image_red = ImageDraw.Draw(Image_red)

    # date_time
    date_time = ''

    def __init__(self):
        logging.debug('Init FetchTelemetry class')        

    ### Application functions
    def fetchTelemetryValuesAndPrintOnImage(self):
        logging.debug('Fetch telemetry values and print them on the main image')
        formatCurrentDate = self.date_time.strftime('%d-%m-%Y')
        response = requests.get(self.url_telemetry+formatCurrentDate)
        json_response = response.json()
        
        if(len(json_response) < 1):
            return

        # Create graphs
        self.createTemperatureGraph(json_response)
        
        # Title
        self.draw_Image_red.rectangle([(0,15), (200,60)], fill = 0, outline = 0, width = 0)
        self.draw_Image_red.text((25, 27.5), 'Temp & Humid', font = self.robotoFont_18, fill = 255)

        # Show
        self.draw_Image.text((25, 70), 'Temperature ', font = self.robotoFont, fill = 0)
        self.draw_Image.text((25, 125), 'Humidity ', font = self.robotoFont, fill = 0)
        self.draw_Image.text((240, 70), str(json_response[-1]['temp']), font = self.robotoFont_bold, fill = 0)
        self.draw_Image.text((240, 125), str(json_response[-1]['humid']), font = self.robotoFont_bold, fill = 0)
    
    def createTemperatureGraph(self, telemetry_json_response):
        logging.debug('Create temperature graph')

        # Create plot
        temps = np.array([record['temp'] for record in telemetry_json_response])
        temps = temps.astype(np.float64);
        plt.figure(figsize=(3,2))
        plt.plot(temps, color= "red", linewidth=4)

        # Set axis
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(True)

        # Set ticks and layout -> save afterwards
        plt.yticks(np.arange(min(temps), max(temps) + 1 , step=0.5))        
        plt.tight_layout()
        plt.savefig(os.path.join(self.picdir, 'tempGraph.png'))

        # Place graph on the red image
        graph = Image.open(os.path.join(self.picdir, 'tempGraph.png'))
        self.Image_red.paste(graph, (10,185))

    def fetchCryptos(self):
        logging.debug('Fetch cryptos and print them on image')

        try:
            response = requests.get(self.url_crypto)
            crypto_response = response.json()

            logging.debug('Create crypto dict')
            cryptoListToPrint = ['ADA-EUR', 'MANA-EUR', 'ETH-EUR', 'ETC-EUR', 'LTC-EUR', 'BTC-EUR'];
            dict = {}
            for crypto in crypto_response:
                if crypto['market'] in cryptoListToPrint:
                    dict[crypto['market']] = crypto['price'];

            # Draw a rectangle
            self.draw_Image.rectangle([(440,35), (680,60)], fill = 0, outline = 0, width = 0)
            self.draw_Image.rectangle([(440,60), (880,528)], fill = 0, outline = 0, width = 0)
            self.draw_Image.text((475, 40), 'Crypto', font =  self.train_one, fill = 255)

            # Bitcoin
            self.draw_Image.text((475, 125), 'Bitcoin', font=  self.robotoFont, fill = 255)
            self.draw_Image.text((725, 125), dict['BTC-EUR'], font =  self.robotoFont_bold, fill = 255)

            # Cardano
            self.draw_Image.text((475, 185), 'Cardano', font=  self.robotoFont, fill = 255)
            self.draw_Image.text((725, 185), dict['ADA-EUR'], font =  self.robotoFont_bold, fill = 255)

            # Decentraland
            self.draw_Image.text((475, 245), 'Decentraland', font =  self.robotoFont, fill = 255)
            self.draw_Image.text((725, 245), dict['MANA-EUR'], font =  self.robotoFont_bold, fill = 255)

            # Etherium
            self.draw_Image.text((475, 305), 'Etherium', font=  self.robotoFont, fill = 255)
            self.draw_Image.text((725, 305), dict['ETH-EUR'], font =  self.robotoFont_bold, fill = 255)

            # Etherium Classic
            self.draw_Image.text((475, 365), 'Eth. Classic', font=  self.robotoFont, fill = 255)
            self.draw_Image.text((725, 365), dict['ETC-EUR'], font =  self.robotoFont_bold, fill = 255)

            # Litecoin
            self.draw_Image.text((475, 425), 'Litecoin', font=  self.robotoFont, fill = 255)
            self.draw_Image.text((725, 425), dict['LTC-EUR'], font =  self.robotoFont_bold, fill = 255)

        except:
            logging.log('An error occured while fetching the cryptos')
            logging.exception(traceback.extract_stack)

    def createClock(self):
        logging.debug('Creating clock')
        self.date_time = datetime.now()
        self.draw_Image_red.rectangle([(680,15), (880,60)], fill = 0, outline = 0, width = 0)
        self.draw_Image_red.text((705, 27.5), self.date_time.strftime('%a %d %b. %H:%M'), font = self.robotoFont_18, fill = 255)
    
    def createImage(self):
        logging.debug('Function to create image -> contains multiple steps')

        # Init screen
        self.epd.init()

        # Clear out current screen
        self.epd.Clear()

        # Create empty images
        self.Image_black = Image.new('1', (self.epd.width, self.epd.height), 255)
        self.Image_red = Image.new('1', (self.epd.width, self.epd.height), 255)
        self.draw_Image = ImageDraw.Draw(self.Image_black)
        self.draw_Image_red = ImageDraw.Draw(self.Image_red)

        # Wait some time to make sure the screen is clear
        time.sleep(15)

        self.createClock()

        self.fetchTelemetryValuesAndPrintOnImage()

        self.fetchCryptos()        

        time.sleep(2)

        self.epd.display(self.epd.getbuffer(self.Image_black), self.epd.getbuffer(self.Image_red))

        time.sleep(20)

        logging.debug('Main function completed...')
        self.epd.sleep()               

    def start(self):
        logging.debug('starting while True function')
        while(True):
            self.createImage()

            time.sleep(550)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        ft = fetchTelemetry()
        logging.debug('starting application')
        ft.start()
    except:
        logging.exception(traceback.extract_stack)
        ft.epd.sleep()
        logging.error('closing application!')