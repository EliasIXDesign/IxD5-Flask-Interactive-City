from flask import Flask, render_template, redirect, url_for
import time
import threading
import pyautogui
import qrcode 
from PIL import Image 
import base64
import io
import numpy as np 


app = Flask(__name__)

inp = ""
selectedQuestion = "How many times is the word electric cars used"
selectedAnswer = 5 #position in cap array int from 1 to 10

@app.before_first_request
def activate_job():
    def run_job():
        global inp

        with app.app_context(), app.test_request_context():
            while True:
                print("Run recurring task")
                time.sleep(7)
                inp = "q1"
                pyautogui.hotkey('f5')

    def run_job2():
        global inp

        with app.app_context(), app.test_request_context():
            while True:
                print("Run recurring task2")
                time.sleep(9)
                inp = "q2"
                pyautogui.hotkey('f5')


    thread = threading.Thread(target=run_job)
    thread.start()
    thread2 = threading.Thread(target=run_job2)
    thread2.start()


@app.route("/")
def index():
	global inp

	if inp == "q1" :
		return redirect(url_for("question"))

	elif inp == "q2" : 
		return render_template("index2.html")

	else: 
		return render_template("index2.html")


@app.route("/question")
def question():
	global inp


	array = np.genfromtxt(r'QuestionsBaseOne.txt', dtype=str, delimiter=",")

	oplist = array[0][2:12]

	if inp == "q1" :
		return render_template("qtest.html", options = oplist)

	elif inp == "q2" : 
		return redirect(url_for("index"))

	else: 
		return render_template("index2.html")


@app.route("/q1") #this is now the qr code screen
def q1():

	qrselectedquestion = selectedQuestion 
	qrselectedanswer = str(selectedAnswer)
	encodedQR = qrselectedquestion.replace(" ", "%20") 
	print(encodedQR)

	##Need to use one % more at each %20 in order to escape the first %s
	##So coloring is fucked up
	qrlink = "https://www.aalborg.dk/51934?view=cm&68c963d3-3785-410b-bf46-294cd436ff8c=%s%%20And%%20I%%20Answered%%20:%s&fs=1.aspx" % (encodedQR, qrselectedanswer)


	img = qrcode.make(qrlink)

	type(img)

	imgname = selectedQuestion + str(selectedAnswer)

	filename = "%s.png" % imgname

	img.save(filename)


	

	##Open image to display 
	
	im = Image.open(filename)
	
	data = io.BytesIO()
	
	im.save(data, "PNG")
	
	encoded_img_data = base64.b64encode(data.getvalue())



	##NAVIGATION
	if inp == "q1" :
		return render_template("infoqr.html", img_data=encoded_img_data.decode('utf-8'))

	elif inp == "q2" : 
		return redirect(url_for("index"))

	else: 
		return render_template("index2.html")

	



if __name__ == "__main__":

	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run()


