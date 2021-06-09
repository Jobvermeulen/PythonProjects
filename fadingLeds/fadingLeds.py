import time
from gpiozero import PWMLED
import numpy as np

# Set-up LEDs
led_green = PWMLED(23)
# led_yellow = PWMLED(27)
led_orange = PWMLED(25)
# led_blue = PWMLED(10)

def main():
    fade_arr_up = np.arange(0.0, 1.0, 0.005)
    fade_arr_down = np.arange(1.0, 0, -0.005)
    while True:
        # Light up
        for fade in fade_arr_up:
            print("Light up: ", fade)
            led_green.value = fade
            led_orange.value = fade
            time.sleep(0.1)
        
        # Wait 500 milliseconds 
        time.sleep(0.5)

        # Light fade out
        for fade in fade_arr_down:
            print("Fade out: ",fade)
            led_green.value = fade
            led_orange.value = fade
            time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    except:
        led_green.close()
        led_orange.close()