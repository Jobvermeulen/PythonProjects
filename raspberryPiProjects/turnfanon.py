import RPi.GPIO as GPIO
import sys, getopt

PINNUMBER = 12

def main():
    try:
        opts, args = getopt.getopt(argv,"hf:",["fan="])
    except getopt.GetoptError:
        print('fancontrol -f <True / false>')
        sys.exit(2)

    # INIT GPIO HEADER WITH FAN PINNNUMBER
    GPIO.setwarnings(false)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PINNUMBER, GPIO.OUT, initial=GPIO.LOW)

    for opt, arg in opts:
        if opt == '-h':
            print('fancontrol -f <True / false>')
            sys.exit()
        elif opt in ("-f", "--fan"):
            fanBool = arg
            if(type(fanBool) == bool):
                GPIO.output(PINNUMBER,GPIO.HIGH)
            else:
                sys.exit()

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except:
        GPIO.cleanup()