import sys
import os
import requests
from requests.models import Response
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
# libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)

import logging
import epd7in5b_HD

import time
from PIL import Image,ImageDraw,ImageFont
import traceback

def main(response:Response):
    try:
        epd = epd7in5b_HD.EPD()
        #epd = epd7in5b_V2.EPD()

        logging.info("init and Clear!")
        epd.init()
        epd.Clear()
        
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        Other = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw_Himage = ImageDraw.Draw(Himage)
        draw_other = ImageDraw.Draw(Other)

        draw_Himage.text((10, 0), 'Temp' + str(response['temp']), font = font24, fill = 0)
        draw_Himage.text((10, 20), 'Humid' +  str(response['humid']), font = font24, fill = 0)
        
        # draw_Himage.text((10, 0), 'hello world', font = font24, fill = 0)
        # draw_Himage.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
        # draw_Himage.text((150, 0), u'微雪电子', font = font24, fill = 0)    
        # draw_other.line((20, 50, 70, 100), fill = 0)
        # draw_other.line((70, 50, 20, 100), fill = 0)
        # draw_other.rectangle((20, 50, 70, 100), outline = 0)
        # draw_other.line((165, 50, 165, 100), fill = 0)
        # draw_Himage.line((140, 75, 190, 75), fill = 0)
        # draw_Himage.arc((140, 50, 190, 100), 0, 360, fill = 0)
        # draw_Himage.rectangle((80, 50, 130, 100), fill = 0)
        # draw_Himage.chord((200, 50, 250, 100), 0, 360, fill = 0)


        epd.display(epd.getbuffer(Himage),epd.getbuffer(Other))
        time.sleep(2)
        epd.sleep()
        
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5b_HD.epdconfig.module_exit()
        exit()

def requestData():
    response = requests.get('http://192.168.1.6:3000/v1/telemetrylatest')
    json_response = response.json()
    return json_response

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG)
        response = requestData()
        logging.debug(response)
        main(response)

    except:
        logging.info('Something went wrong!')
