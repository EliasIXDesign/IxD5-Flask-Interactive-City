from flask import Flask, render_template, redirect, url_for
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
state = "index" # reveal, base1, base2, index 
lastTouch = 0 #used for animation and for selectedAnswer
lastTouchIndex = "" 
selectedQuestion = ""
answer = "" #float from 1 to 10 
selectedAnswer = "" #position in cap array int from 1 to 10
widthVar = 0
selecOp = 0
questionloop = 0
revealtext = ""
region = ""


listBaseOne = np.genfromtxt(r'QuestionsBaseOne.txt', dtype=str, delimiter=",")
listBaseTwo = np.genfromtxt(r'QuestionsBaseTwo.txt', dtype=str, delimiter=",")

oplist = listBaseOne[0][3:13] ##takes a default from base1 q1 so that there's no error from turbo flask bc empty

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


##==================================================================##
#
#
#
#
#
#⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣠⣤⣶⣶
#⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢰⣿⣿⣿⣿
#⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣾⣿⣿⣿⣿
#⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿
#⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿
#⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿
#⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿
#⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿
#⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿
#⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿
#⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿
#⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿
#⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿
#⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿
#
#
#
#
#
#
##==================THREADS================================================##

@app.before_first_request
def activate_job():
    def capTouchBar(): #update cap touch bar graph
        global widthVar, lastTouch, selecOp
        with app.app_context():
            while True:
                if mpr121[0].value:
                    widthVar = 100
                    lastTouch = widthVar
                    selecOp = oplist[0]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 1)
                    colorWipe(strip, Color(0, 0, 255), 1)
                    print(0)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))

                elif mpr121[1].value:
                    widthVar = 200
                    lastTouch = widthVar
                    selecOp = oplist[1]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 2)
                    colorWipe(strip, Color(0, 0, 255), 2)
                    print(1)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))
            

                elif mpr121[2].value:
                    widthVar = 300
                    lastTouch = widthVar
                    selecOp = oplist[2]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 3)
                    colorWipe(strip, Color(0, 0, 255), 3)
                    print(2)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))
             

                elif mpr121[3].value:
                    widthVar = 400
                    lastTouch = widthVar
                    selecOp = oplist[3]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 4)
                    colorWipe(strip, Color(0, 0, 255), 4)
                    print(3)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))
                    

                elif mpr121[4].value:
                    widthVar = 500
                    lastTouch = widthVar
                    selecOp = oplist[4]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 5)
                    colorWipe(strip, Color(0, 0, 255), 5)
                    print(4)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))
            

                elif mpr121[5].value:
                    widthVar = 600
                    lastTouch = widthVar
                    selecOp = oplist[5]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 6)
                    colorWipe(strip, Color(0, 0, 255), 6)
                    print(5)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))
            

                elif mpr121[6].value:
                    widthVar = 700
                    lastTouch = widthVar
                    selecOp = oplist[6]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 7)
                    colorWipe(strip, Color(0, 0, 255), 7)
                    print(6)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))
            

                elif mpr121[7].value:
                    widthVar = 800
                    lastTouch = widthVar
                    selecOp = oplist[7]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 8)
                    colorWipe(strip, Color(0, 0, 255), 8)
                    print(7)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))
            

                elif mpr121[8].value:
                    widthVar = 900
                    lastTouch = widthVar
                    selecOp = oplist[8]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 9)
                    colorWipe(strip, Color(0, 0, 255), 9)
                    print(8)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))
            

                elif mpr121[9].value:
                    widthVar = 1000
                    lastTouch = widthVar
                    selecOp = oplist[9]
                    lastTouchIndex = selecOp
                    colorWipeAll(strip, 10)
                    colorWipe(strip, Color(0, 0, 255), 10)
                    print(9)
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))
            

                else: 
                    widthVar = lastTouch
                    selecOp = lastTouchIndex 
                    turbo.push(turbo.replace(render_template('loadcap.html'), 'widthVar'))
                    turbo.push(turbo.replace(render_template('selectedoption.html'), 'selecOp'))    



    def comWithArduino(): #update global state variable 
        global state

        with app.app_context():
            while True:
                if ser.in_waiting > 0:
                    ardustate = ser.readline().decode('utf-8').rstrip() #we recieve bytes to we decode to string
                    state = ardustate
                    print(state)
                    pyautogui.hotkey('f5') #refreshes page by pressing F5

                


    # Starts the threads
    thread = threading.Thread(target=capTouchBar)
    thread.start()
    thread2 = threading.Thread(target=comWithArduino) 
    thread2.start()


##From flask, updates variables in a html tempalte without reloading page, used to aniamte bar 
@app.context_processor
def inject_load():
    return {'widthVar': widthVar}

##=================APP ROUTES============================================##

@app.route("/default/") #pick up ball
def default():

    global state

    colorWipe(strip, Color(0, 0, 255), 0) #Wipes all led for reset 


    if state == "base1" :
        return redirect(url_for("question"))

    elif state == "base2" :
        return redirect(url_for("question"))

    elif state == "awaitingball" : 
        return redirect(url_for("awaitingball"))

    elif state == "reveal" :
        return redirect(url_for("reveal"))

    elif state == "default" :
        return render_template("default.html")

    else: 
        return render_template("default.html")
   

@app.route("/awaitingball/") #pick up ball
def awaitingball():

    global state

    colorWipe(strip, Color(0, 0, 255), 0) #Wipes all led for reset 


    if state == "base1" :
        return redirect(url_for("question"))

    elif state == "base2" :
        return redirect(url_for("question"))

    elif state == "awaitingball" : 
        return render_template("awaitingball.html")

    elif state == "reveal" :
        return redirect(url_for("reveal"))

    elif state == "default" :
        return redirect(url_for("default"))

    else: 
        return render_template("index.html")

##=========================QUESTION PAGE=============================##

@app.route("/question/")
def question():
	
    global  selectedAnswer, answer, state, oplist, listBaseOne, listBaseTwo, questionloop, revealtext, lastTouch, region, lastTouchIndex
    

    
    ## Depending on state, select questions from base1 or base2 
    if state == "base1" : 
        question = listBaseOne[questionloop][0]
        revealtext = listBaseOne[questionloop][1]  
        answer = listBaseOne[questionloop][2] 
        oplist = listBaseOne[questionloop][3:13]
        region = "Transport"


    elif state == "base2" :
        question = listBaseTwo[questionloop][0]
        revealtext = listBaseTwo[questionloop][1]  
        answer = listBaseTwo[questionloop][2] 
        oplist = listBaseTwo[questionloop][3:13]
        region = "Culture"

    else : 
        print("Error in reading base 1 or 2 state in question state")


    ##Loops thhrough the questions and then resets when all questions have been displayed
    if questionloop +1 >= len(listBaseOne[0]) : #+1 because len starts at 1 and not 0 
        questionloop = 0

    else : 
        questionloop = questionloop +1


    ##Last cap touch pad to be touched before state changes is the selected answer 
    selectedAnswer = lastTouchIndex



    


    ##NAVIGATION
    if state == "base1" :
        return render_template("question.html", question = question, options = oplist, region = region )

    elif state == "base2" :
        return render_template("question.html", question = question, options = oplist, region = region)

    elif state == "default" : 
        return redirect(url_for("default"))

    elif state == "reveal" :
        return redirect(url_for("reveal"))

    elif state == "awaitingball" : 
        return redirect(url_for("awaitingball"))

    else: 
        return render_template("question.html", options = oplist, question = question)




##=======================REVEAL PAGE===============================##
@app.route("/reveal/")
def reveal():
    
    global selectedQuestion, selectedAnswer, answer, state, revealtext,

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
        return render_template("reveal.html", img_data=encoded_img_data.decode('utf-8'))#, 
            #selectedQuestion = selectedQuestion, answer = answer, selectedAnswer = selectedAnswer)

    elif state == "base1" :
        return redirect(url_for("question"))

    elif state == "base2" : 
        return redirect(url_for("question"))

    elif state == "default" : 
        return redirect(url_for("default"))

    elif state == "awaitingball" : 
        return redirect(url_for("awaitingball"))

    else: 
        return render_template("reveal.html", img_data=encoded_img_data.decode('utf-8'))







##=====================PROGRAM================================================##



if __name__ == "__main__":

	app.run()


