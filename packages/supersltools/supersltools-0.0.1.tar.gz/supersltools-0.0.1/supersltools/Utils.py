import smtplib, ssl
import tkinter
import time
import random
import turtle
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from gtts import gTTS 
import os
import smtplib, ssl
import speech_recognition as sr
import playsound



def HelloWorld():
	print("Hello world")

def tables():
	for i in range(int("starting number:  "), int("ending number:  ")):
		for j  in range(int("starting number:  "), int("ending number:  ")):
			print(str(i) + "x"+ str(j) + "=" + str(i*j))
		print("~~~~~~~~~~")

def SimpleIntrest():
	p = float(input("enter the principal:  "))
	r = float(input("enter the rate: "))
	t = float(input("enter the time:  "))

	amount = ((p*r*t)/100) + p
	intrest = amount - p

	print(f"here is the amount: {amount} ")
	print(f"here is the intrest: {intrest}")

def CompoundIntrest():
	principal = float(input("Enter the principle:  "))
	rate = float(input("Enter the rate:  "))/ 100
	time = float(input("Enter the Time period:  "))

	amount = principal*((1 + rate)**time)
	ci = amount - principal

	print(f"Here is your amount: {amount} ")
	print(f" Here is the compound intrest calculated : {ci}")

def SendMail():

	sender = input("enter sender's email adress:")
	password = input("enter your gmail password:")
	rec = input("enter the reciever's email adress:")
	message = input("enter your message: ")
	def send():
		port = 465
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
			print("sending...")
			server.login(sender, password)
			server.sendmail(sender, rec, message)
			print("Done!")

	send()

def SendGuiMail():
	screen = tkinter.Tk()

	label1 = tkinter.Label(text = "Enter sender's email adress:  ")
	label1.pack()

	entry1 = tkinter.Entry( borderwidth = 5 )
	entry1.pack()

	label2 = tkinter.Label(text = "Enter reciever's email adress:  ")
	label2.pack()

	entry2 = tkinter.Entry(borderwidth = 5)
	entry2.pack()

	label3 = tkinter.Label("Enter sender's gmail password:  ")
	label3.pack()

	entry3 = tkinter.Entry(borderwidth  = 5)
	entry3.pack()

	label4 = tkinter.Label(text = "What do you wanna say?:  ")
	label4.pack()

	entry4 = tkinter.Entry(borderwidth = 5)
	entry4.pack()

	def send():
		sender = entry1.get()

		password = entrt3.get()

		reciever = entry2.get()

		message = entry4.get()
		port = 465

		label5 = tkinter.Label(text = "Sending...")
		label5.pack()

		context = ssl.create_default_context()
		with SMTP_SSL("mtp.gmail.com", port, context = context) as server:
			server.login(sender, password)
			server.sendmail(sender, reciever, message)
			label6 = tkinter.Label(text = "Sent!!!")
			label6.pack()

	button1 = tkinter.button(text = "Send", command= send)
	button1.pack()
	screen.mainloop()

def SnakeGame():
	delay = 0.1
	wn = turtle.Screen()
	wn.title("Snake Game")
	wn.bgcolor("green")
	wn.setup(width=600, height=600)
	wn.tracer(0)
	head=turtle.Turtle()
	head.speed(0)
	head.shape("square")
	head.color("black")
	head.penup()
	head.goto(0,0)
	head.direction ="stop"

	food=turtle.Turtle()
	food.speed(0)
	food.shape("circle")
	food.color("blue")
	food.penup()
	food.goto(0,0)
	segments=[]
	def move():
	    if head.direction =="up":
	        y =head.ycor()
	        head.sety(y + 20)
	    if head.direction =="down":
	        y =head.ycor()
	        head.sety(y - 20)
	    if head.direction =="left":
	        x =head.xcor()
	        head.setx(x- 20)

	    if head.direction =="right":
	        x =head.xcor()
	        head.setx(x + 20)


	def go_up():
	    head.direction = "up"
	def go_down():
	    head.direction = "down"
	def go_right():
	    head.direction = "right"
	def go_left():
	    head.direction = "left"

	wn.listen()
	wn.onkeypress(go_up,"Up")
	wn.onkeypress(go_down,"Down")
	wn.onkeypress(go_left,"Left")
	wn.onkeypress(go_right,"Right")
	#main game loop
	while True:
	     wn.update()
	     if head.distance(food)<20:
	         x = random.randint(-290,290)
	         y = random.randint(-290,290)
	         food.goto(x,y)


	         new_segment = turtle.Turtle()
	         new_segment.speed(0)
	         new_segment.shape("square")
	         new_segment.color("black")
	         new_segment.penup()
	         segments.append(new_segment)

	     for index in range(len(segments)-1,0,-1):
	        x= segments[index-1].xcor()
	        y= segments[index-1].ycor()
	        segments[index].goto(x,y)

	     if len(segments)>0:
	        x=head.xcor()
	        y=head.ycor()
	        segments[0].goto(x,y)

	     move()

	     for segment in segments:
	         if segment.distance(head)<20:
	             time.sleep(0.1)
	             head.goto(0,0)
	             head.direction = "stop"
	     time.sleep(delay )


	wn.mainloop()


def Talk_to_alexa():

	listener = sr.Recognizer()
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)

	paths ={"chemistry" : "https://zoom.us/j/2018700227?pwd=Y253bnBkVUVOVytYcFhwRU85ZGtndz09",
	        "maths" : "https://zoom.us/j/5353201805?pwd=bzBXVkZ3OXkwWmdwM1NySkpBZHBWdz09",
	        "Maths" : "https://zoom.us/j/5353201805?pwd=bzBXVkZ3OXkwWmdwM1NySkpBZHBWdz09",
	        "mathematics" : "https://zoom.us/j/5353201805?pwd=bzBXVkZ3OXkwWmdwM1NySkpBZHBWdz09",
	        "English" : "https://us04web.zoom.us/j/2063298864?pwd=eGdoOVdQc3MwaHRsS3QvaFpmWnFZZz09",
	        "geography" : "https://zoom.us/j/6531783499?pwd=R05MMmVHbWdJcE5iZjZUWkFUSVZadz09",
	        "Geography" : "https://zoom.us/j/6531783499?pwd=R05MMmVHbWdJcE5iZjZUWkFUSVZadz09",
	        "CLT": "https://zoom.us/j/8396643447?pwd=N0xjSFpzNXhjSm4yeUZaVnZNYzR2QT09",
	        "clt": "https://zoom.us/j/8396643447?pwd=N0xjSFpzNXhjSm4yeUZaVnZNYzR2QT09",
	        "physics" : "https://zoom.us/j/8396643447?pwd=N0xjSFpzNXhjSm4yeUZaVnZNYzR2QT09",
	        "Hindi" : "https://zoom.us/j/7268866920?pwd=VFJqbVVFZzRvQjUvNUt0ZmRRWW00dz09",
	        "culture" : "https://us02web.zoom.us/j/5551032554?pwd=NmlEb0p6OVI2bmloY3dFNmJOemRjZz09",
	        "biology" : "https://zoom.us/j/8172656837?pwd=NUZya2JMVnpLc3RnTHlpVytWTVdiQT09",
	        "history" : "https://zoom.us/j/3773344786?pwd=YXhsaDFhQUdZd0NvYkU4NllBY2x3Zz09",
	        "mail" : "https://mail.google.com/mail/u/0/#inbox",
	        "youtube" : "https://youtube.com",
	        "amresh sir" : "https://us04web.zoom.us/j/2063298864?pwd=eGdoOVdQc3MwaHRsS3QvaFpmWnFZZz09",
	        "shanmugavel  akka" :"https://zoom.us/j/5353201805?pwd=bzBXVkZ3OXkwWmdwM1NySkpBZHBWdz09",
	        "jyoti akka" : "https://zoom.us/j/2018700227?pwd=Y253bnBkVUVOVytYcFhwRU85ZGtndz09",
	        "upasna akka" : "https://zoom.us/j/3773344786?pwd=YXhsaDFhQUdZd0NvYkU4NllBY2x3Zz09",
	        "alok sir" : "https://zoom.us/j/7268866920?pwd=VFJqbVVFZzRvQjUvNUt0ZmRRWW00dz09",
	        "arun sir" : "https://zoom.us/j/8396643447?pwd=N0xjSFpzNXhjSm4yeUZaVnZNYzR2QT09",
	        "personal-mail" : "https://mail.google.com/mail/u/1/#inbox",
	        "art" : "https://zoom.us/j/8095609676?pwd=aEdlRVBJdUVuMFhsTW0vLzB1ejVZdz09",
	        "arts and craft": "https://zoom.us/j/8095609676?pwd=aEdlRVBJdUVuMFhsTW0vLzB1ejVZdz09",
	        "me" : "snehashish.laskar@gmail.com"}

	contact  = ["Ishan", "ishan", "mom", "Mom", "dad", "Dad", "amresh sir" ," Amresh sir", "mamu", "mamu", "myself"]

	contact_with_email  = {"mamu" : "nickadlakha@gmail.com","myself" : "snehashish.laskar@sahyadrischool.org", "ovee": "ovee.khemani@sahyadrischool.org", "ishan" : "ishan.kashyap@sahyadrischool.org", "dad":"sumanlaskar1@gmail.com", "Dad" : "sumanlaskar1@gmail.com"}


	def talk(text):

	    engine.say(text)

	    engine.runAndWait()


	def take_command():

	    try:

	        with sr.Microphone() as source:
	            print('listening...')
	            voice = listener.listen(source)
	            command = listener.recognize_google(voice)
	            command = command.lower()
	            if 'alexa' in command:
	                command = command.replace('alexa', '')
	                print(command)
	    except:
	        pass
	    return command


	def run_alexa():
	    command = take_command()
	    print(command)
	    if "your name" in command:
	        talk("my name is AVA!")

	    elif "what can you do" in command:
	            talk("talk to you boss!")

	    elif "my brother" in command:
	            talk("your brother is snehamoy")

	    elif "hello" in command:
	            talk("hello boss")

	    elif "hai" in command:
	            talk("hi boss")

	    elif"hay" in command:
	            talk("hey boss")

	    elif "music" in command:
	            talk("Sure sir!")
	            os.startfile("https://www.youtube.com/watch?v=ShZ978fBl6Y&list=RDShZ978fBl6Y&start_radio=1")

	    elif "YouTube" in command:
	            talk("opening!")
	            os.startfile("https://www.youtube.com")

	    elif "youtube" in command:
	        talk("opening sir!")
	        os.startfile("https://www.youtube.com")

	    elif "Gmail" in command:
	            talk("yes boss")
	            os.startfile("https://mail.google.com/mail/u/0/#inbox")

	    elif "spotify" in command:
	            talk("music time!")
	            os.startfile("https://open.spotify.com/playlist/4Bq5OXOO9qTh5Lzh2hSQOr")

	    elif "Spotify" in command:
	            talk("music time!")
	            os.startfile("https://open.spotify.com/playlist/4Bq5OXOO9qTh5Lzh2hSQOr")

	    elif "Chemistry" in command:
	            talk("yes boss!")
	            os.startfile("https://zoom.us/j/2018700227?pwd=Y253bnBkVUVOVytYcFhwRU85ZGtndz09")

	    elif "chemistry" in command:
	            talk("yes boss!")
	            os.startfile("https://zoom.us/j/2018700227?pwd=Y253bnBkVUVOVytYcFhwRU85ZGtndz09")

	    elif "maths" in command:
	            talk("yes boss!")
	            os.startfile("https://zoom.us/j/5353201805?pwd=bzBXVkZ3OXkwWmdwM1NySkpBZHBWdz09")

	    elif "mathematics" in command:
	            talk("yes boss")
	            os.startfile("https://zoom.us/j/5353201805?pwd=bzBXVkZ3OXkwWmdwM1NySkpBZHBWdz09")

	    elif "Mathematics" in command:
	            talk("yes boss")
	            os.startfile("https://zoom.us/j/5353201805?pwd=bzBXVkZ3OXkwWmdwM1NySkpBZHBWdz09")

	    elif "maps" in command:
	            talk("yes boss!")
	            os.startfile("https://zoom.us/j/5353201805?pwd=bzBXVkZ3OXkwWmdwM1NySkpBZHBWdz09")

	    elif "wish" in command:
	        talk("Happy Birthday to you! happy birthday to you! happy birthday dear suman happy birthday to you!")

	    elif "English" in command:
	            talk("yes boss!")
	            os.startfile(paths.get("English"))

	    elif "english" in command:
	            talk("yes boss!")
	            os.startfile(paths.get("English"))

	    elif "Physics" in command:
	            talk("yes boss!")
	            os.startfile(paths.get("physics"))

	    elif"physics" in command:
	            talk("yes boss!")
	            os.startfile(paths.get("physics"))

	    elif "CLT" in command:
	            talk("yes boss!")
	            os.startfile(paths.get("CLT"))

	    elif "personal mail" in command:
	            talk("ok Boss!")
	            os.startfile(paths.get("personal-mail"))

	    elif "Hindi" in command:
	            talk("yes boss!")
	            os.startfile(paths.get("Hindi"))

	    elif "hindi" in command:
	            talk("Yes boss!")
	            os.startfile(paths.get("Hindi"))

	    elif "bio" in command:
	            talk("Yes Boss!")
	            os.startfile(paths.get("biology"))

	    elif "biology" in command:
	            talk("Ok boss!")
	            os.startfile(paths.get("biology"))

	    elif "history" in command:
	            talk("Ok boss!")
	            os.startfile(paths.get("history"))

	    elif "culture" in command:
	            talk("Yes boss!")
	            os.startfile(paths.get("culture"))

	    elif "art" in command:
	            talk("Yes Boss!")
	            os.startfile(paths.get("art"))

	    elif "geography" in command:
	            talk("Yes Boss!")
	            os.startfile(paths.get("geography"))

	    elif "Geography" in command:
	            talk("Yes boss")
	            os.startfile(paths.get("geography"))

	    elif "calculator" in command:
	            os.startfile("C:/Windows/System32/calc.exe")

	    elif "hi" in command:
	            talk("hi Boss!") 


	    elif "welcome" in command:
	            talk("welcome to our house ! nice to meet you")

	    elif "go" in command:
	            exit()

	    elif "compose" in command:
	            talk("to whom sir?")
	            r = sr.Recognizer()
	            print("listening.....")

	            with sr.Microphone() as source:
	                    audio1 = r.listen(source)
	                    command1 = ""
	                    command1 = r.recognize_google(audio1)

	            if command1 in contact:
	                    talk("what do you wanna say sir?")
	                    r = sr.Recognizer()
	                    print("listening.....")

	                    with sr.Microphone() as source:
	                            audio2 = r.listen(source)
	                            command2 = ""
	                            command2 = r.recognize_google(audio2)
	                            
	                    message = command2
	                    re1 = contact_with_email.get(command1)
	                    sender = "snehashish.laskar@gmail.com"
	                    password = "guitar08036"
	                    port = 465
	                    context = ssl.create_default_context()
	                    with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
	                            server.login(sender, password)
	                            server.sendmail(sender, re1, command2)
	                            talk("done sir!")
	    
	    elif "sleep" in command:
	        talk("okay sir turning off line")
	        quit()

	    elif "get lost" in command:
	        talk("okay sir turning offline")
	        quit()
	    elif "play rock":
	    	playsound.playsound("C:/Users/sneha/Music/rock.mp3")


	    elif "go away" in command:
	        talk("okay sir turning offline")
	        quit()

	    elif "off line" in command:
	        talk("okay sir! turning offline")
	        quit()

	    elif "good morning" in command:
	        talk("good morning boss!")

	    elif "Good Morning" in command:
	        talk("Good morning sir!")
	            
	    elif "Good morning" in command:
	        talk("good morning sir!")

	    elif "sorry" in command:
	        talk("its okay sir!")

	    elif "Sorry" in command:
	        talk("its okay sir")
	    
	    elif 'joke' in command:
	        talk(pyjokes.get_joke())



	    elif 'play' in command:
	        song = command.replace('play', '')
	        talk('playing ' + song)
	        pywhatkit.playonyt(song)
	    
	    elif 'time' in command:
	        time = datetime.datetime.now().strftime('%I:%M %p')
	        talk('Current time is ' + time)
	    
	    elif 'search' in command:
	        person = command.replace('search', '')
	        info = wikipedia.summary(person, 1)
	        print(info)
	        talk(info)

	    else:
	            talk("i don't get you, that's not in my list of commands")

	while True:
	    run_alexa()


