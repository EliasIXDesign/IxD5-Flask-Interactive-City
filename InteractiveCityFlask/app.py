from flask import Flask, render_template
import time
import board
import busio
# Import MPR121 module.
import adafruit_mpr121
import threading 
from turbo_flask import Turbo
########LED's########
from rpi_ws281x import *
import argparse


# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)


# LED strip configuration:
LED_COUNT      = 10      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 155     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

lastTouch = 0

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def colorWipe(strip, color, pos):
    """Wipe color across display a pixel at a time."""
    for i in range(pos):
        strip.setPixelColor(i, color)
        strip.show()
    #time.sleep(wait_ms/1000.0)

def colorWipeAll(strip, pos):
    """Wipe color across display a pixel at a time."""
    for i in range(pos, 10):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        #time.sleep(wait_ms/1000.0)

app = Flask(__name__)
turbo = Turbo(app)

@app.context_processor
def inject_load():

	global lastTouch


	if mpr121[0].value:
			widthVar = 100
			lastTouch = widthVar
			colorWipeAll(strip, 1)
			colorWipe(strip, Color(0, 255, 0), 1)
			print(0)
			return {'widthVar': widthVar}

	elif mpr121[1].value:
			widthVar = 200
			lastTouch = widthVar
			colorWipeAll(strip, 2)
			colorWipe(strip, Color(0, 255, 0), 2)
			print(1)
			return {'widthVar': widthVar} 

	elif mpr121[2].value:
			widthVar = 300
			lastTouch = widthVar
			colorWipeAll(strip, 3)
			colorWipe(strip, Color(0, 255, 0), 3)
			print(2)
			return {'widthVar': widthVar} 

	elif mpr121[3].value:
			widthVar = 400
			lastTouch = widthVar
			colorWipeAll(strip, 4)
			colorWipe(strip, Color(0, 0, 255), 4)
			print(3)
			return {'widthVar': widthVar}

	elif mpr121[4].value:
			widthVar = 500
			lastTouch = widthVar
			colorWipeAll(strip, 5)
			colorWipe(strip, Color(0, 0, 255), 5)
			print(4)
			return {'widthVar': widthVar} 

	elif mpr121[5].value:
			widthVar = 600
			lastTouch = widthVar
			colorWipeAll(strip, 6)
			colorWipe(strip, Color(0, 0, 255), 6)
			print(5)
			return {'widthVar': widthVar}

	elif mpr121[6].value:
			widthVar = 700
			lastTouch = widthVar
			colorWipeAll(strip, 7)
			colorWipe(strip, Color(255, 0, 0), 7)
			print(6)
			return {'widthVar': widthVar}

	elif mpr121[7].value:
			widthVar = 800
			lastTouch = widthVar
			colorWipeAll(strip, 8)
			colorWipe(strip, Color(255, 0, 0), 8)
			print(7)
			return {'widthVar': widthVar}

	elif mpr121[8].value:
			widthVar = 900
			lastTouch = widthVar
			colorWipeAll(strip, 9)
			colorWipe(strip, Color(255, 0, 0), 9)
			print(8)
			return {'widthVar': widthVar}

	elif mpr121[9].value:
			widthVar = 1000
			lastTouch = widthVar
			colorWipeAll(strip, 10)
			colorWipe(strip, Color(255, 0, 0), 10)
			print(9)
			return {'widthVar': widthVar}

	else: 
			widthVar = lastTouch	
			return {'widthVar': widthVar}



###########################################################################




@app.route("/")
def index():


	return render_template("index.html")



@app.route("/Q1/")
def index():
	return render_template("Q1.html")

@app.route("/Q2/")
def index():
	return render_template("Q2.html")


#######################################################################
@app.route("/test/")
def indextest():
	  # If you're curious or want to see debug info for each pin, uncomment the
    # following lines:
        # If you're curious or want to see debug info for each pin, uncomment the
    # following lines:
    while True:
        print ('\t\t\t\t\t\t\t\t\t\t\t\t\t 0x{0:X}'.format(mpr121.touched()))
        filtered = [mpr121.filtered_data(i) for i in range(12)]
        print ('Filt:', '\t'.join(map(str, filtered)))
        base = [mpr121.baseline_data(i) for i in range(12)]
        print ('Base:', '\t'.join(map(str, base)))
        time.sleep(0.05)
        	
#########################################################################



@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


def update_load():
    with app.app_context():
        while True:
            time.sleep(0.05)
            turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))


#add if main == 
#and also in that function here run the if int = 1, redirect url to Q1??
app.run ()
