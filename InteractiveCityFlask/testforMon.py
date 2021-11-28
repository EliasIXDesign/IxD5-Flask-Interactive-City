from flask import Flask, render_template
import time
import board
import busio
import serial
import random
import numpy as np 
# Import MPR121 module.
import adafruit_mpr121
import threading 
from turbo_flask import Turbo
########LED's########
from rpi_ws281x import *
import argparse
########PAGE REFRESH########
import pyautogui
########QR CODE#########
import qrcode
from PIL import Image 
import base64
import io



##===============VARIABLES==================================##
state = "" # reveal, base1, base2, index 
lastTouch = 0 #used for animation and for selectedAnswer
##For the qr code, from question page to reveal page 
selectedQuestion = ""
answer = "" #float from 1 to 10 
selectedAnswer = "" #position in cap array int from 1 to 10

##==============HARDWARE====================================##
# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object, capacatitive touch.
mpr121 = adafruit_mpr121.MPR121(i2c)


# LED strip configuration:
LED_COUNT      = 10      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

##======================COM WITH ARDUINO==================================##

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

##===================LED Functions=========================================##
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


##============================FLASK==================================##


app = Flask(__name__)
turbo = Turbo(app)

@app.context_processor
def inject_load():

	global lastTouch


	if mpr121[0].value:
			widthVar = 100
			lastTouch = widthVar
			colorWipeAll(strip, 1)
			colorWipe(strip, Color(0, 0, 255), 1)
			print(0)
			return {'widthVar': widthVar}

	elif mpr121[1].value:
			widthVar = 200
			lastTouch = widthVar
			colorWipeAll(strip, 2)
			colorWipe(strip, Color(0, 0, 255), 2)
			print(1)
			return {'widthVar': widthVar} 

	elif mpr121[2].value:
			widthVar = 300
			lastTouch = widthVar
			colorWipeAll(strip, 3)
			colorWipe(strip, Color(0, 0, 255), 3)
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
			colorWipe(strip, Color(0, 0, 255), 7)
			print(6)
			return {'widthVar': widthVar}

	elif mpr121[7].value:
			widthVar = 800
			lastTouch = widthVar
			colorWipeAll(strip, 8)
			colorWipe(strip, Color(0, 0, 255), 8)
			print(7)
			return {'widthVar': widthVar}

	elif mpr121[8].value:
			widthVar = 900
			lastTouch = widthVar
			colorWipeAll(strip, 9)
			colorWipe(strip, Color(0, 0, 255), 9)
			print(8)
			return {'widthVar': widthVar}

	elif mpr121[9].value:
			widthVar = 1000
			lastTouch = widthVar
			colorWipeAll(strip, 10)
			colorWipe(strip, Color(0, 0, 255), 10)
			print(9)
			return {'widthVar': widthVar}

	else: 
			widthVar = lastTouch	
			return {'widthVar': widthVar}


##=================APP ROUTES============================================##

@app.route("/")
def index():

    if : # confirm button pressed 
        pass

    elif : # a base selected with ball
        pass

    elif : # timeout after confirm, return to index
        pass

    elif : # first use or after reset
        return render_template("index.html")

    else : 
        return render_template("index.html")


##=========================QUESTION PAGE=============================##

@app.route("/question/")
def question():
	
    global selectedQuestion, selectedAnswer, answer, state
    # questionText, correctAnswer, op1, op2, op3, op4, op5, op6, op7, op8, op9, op10
    listBaseOne = np.genfromtxt(r'QuestionsBaseOne.txt', dtype=str, delimiter=",")
    listBaseTwo = np.genfromtxt(r'QuestionsBaseTwo.txt', dtype=str, delimiter=",")

    #select random from one of the array depending on state 

    #or maybe just loop through them ? 

    #question 
    question = listBaseOne[0][0]
    question = listBaseTwo[0][0]

    #read Answer
    answer = listBaseOne[0][1]
    answer = listBaseTwo[0][1]
    
    #read possibleAnswers 
    if state == "Base1":
        passoplist = listBaseOne[0][2:12]
    elif state == "Base2":
        oplist = listBaseTwo[0][2:12]


  
    if state == "base1" or "base2" :
        return render_template("qtest.html", options = oplist, question = question)

    elif state == "index" : 
        return redirect(url_for("index"))

    elif state == "reveal" :
        return redirect(url_for("reveal"))

    else: 
        return redirect(url_for("index"))




##=======================REVEAL PAGE===============================##
@app.route("/reveal/")
def reveal():
    
    global selectedQuestion, selectedAnswer, answer, state

    qrselectedquestion = selectedQuestion 
    qrselectedanswer = str(selectedAnswer)
    encodedQR = qrselectedquestion.replace(" ", "%20") 

    ##Need to use one % more at each %20 in order to escape the first %s
    ##So coloring is fucked up
    qrlink = "https://www.aalborg.dk/51934?view=cm&68c963d3-3785-410b-bf46-294cd436ff8c=%s%%20And%%20I%%20Answered%%20:%s&fs=1.aspx" % (encodedQR, qrselectedanswer)


    ##Making the qr code 
    img = qrcode.make(qrlink)

    type(img)

    ##Fills ins variables to name based on what user chose 
    imgname = selectedQuestion + str(selectedAnswer)

    ##Creates the file name replaces %s with var imgname
    filename = "%s.png" % imgname

    ##Saves the file 
    img.save(filename)

    ##Open image to display 
    
    im = Image.open(filename)
    
    ##Converts the image to be passed as variable 
    data = io.BytesIO()
    
    im.save(data, "PNG")
    
    encoded_img_data = base64.b64encode(data.getvalue())


    ##
    ##Converting selected Question, Answer to meaningful test to be displayed



    ##NAVIGATION
    if state == "reveal" :
        return render_template("infoqr.html", img_data=encoded_img_data.decode('utf-8'))

    elif state == "base1" or "base2" :
        return redirect(url_for("question"))

    elif state == "index" : 
        return redirect(url_for("index"))

    else: 
        return redirect(url_for("index"))




##==================THREADS================================================##

@app.before_first_request
def activate_job():
    def capTouchBar(): #update cap touch bar graph
        with app.app_context(), app.test_request_context():
            while True:
                turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))

    def comWithArduino(): #update global state variable 
        global state

        with app.app_context(), app.test_request_context():
            while True:
                if ser.in_waiting > 0:
                    state = ser.readline().decode('utf-8').rstrip() #we recieve bytes to we decode to string
                    pyautogui.hotkey('f5') #refreshes page by pressing F5
                    #update state var
                    #pyautogui.hotkey('f5')
                


    # Starts the threads
    thread = threading.Thread(target=capTouchBar)
    thread.start()
    thread2 = threading.Thread(target=comWithArduino)
    thread2.start()


##=====================PROGRAM================================================##



if __name__ == "__main__":

	app.run ()

