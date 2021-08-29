import csv, os, requests
import tkinter as tk
from random import randint
import time
import threading
import pyttsx3
import ast

#Easy-to-access important variables
DefURL = "https://raw.githubusercontent.com/Tuugboat/MantisCombos/main/Combos.csv" #URL to querry for the updated combo list
Version = "1.0"

#Dealing with the ComboList and ensureing that it is always up to date
def GetCombos(FilePath = "./Combos.csv", header = True):
	#FilePath should direct to a csv file with two columns, the first should be the text to read out the combos and the second should be the wait times for that respective combo.
	Combos = []
	#Open the csv, read the list into Combos
	with open(FilePath) as csvfile:
		CombosList = csv.reader(csvfile)
		for row in CombosList:
			Combos.append(row)
		#Delete the header, if there is one
		if header:
			Combos.pop(0)
		#convert the wait times into integers
		for i in range(len(Combos)):
			Combos[i-1][1] = float(Combos[i-1][1])

		#Check and print. Not useful in practice but useful when running in dev
		for C in Combos:
			if (len(C) != 2) or not (isinstance(C[0], str)) or not (isinstance(C[1], float)):
				print("There is an issue with the following combo: "+C)
	return(Combos)



def UpdateCombos(url = DefURL):
	#attempts to grab combos from the provided url
	try:
		DL = requests.get(url, allow_redirects=True)
		open("Combos.csv", 'wb').write(DL.content)
		return("Combos updated succesfully!")
	except:
		return("Combos not updated")




def RunCombos(SpeechEngine, ComboList, speed, label, flag):
	#This function is meant to be run async from the rest of the program. It should ONLY be called by a thread and ALWAYS with a refrenceable flag
	while flag.is_set():
		Selection = randint(0, len(ComboList)-1) #Randomly select an index
		
		ToText = ComboList[Selection][0].upper().replace(" ", "\n") #Config the string to the required format for showing in the window
		label.configure(text=ToText) #Configures the passed-through label
		
		#Speak and wait the combo/wait time, adjusted for speed
		SpeechEngine.say(ComboList[Selection][0])
		SpeechEngine.runAndWait()
		time.sleep(ComboList[Selection][1]/(max(speed, 0.1)))



#-----------------------------GUI-----------------------------------------
class AppWindow(tk.Tk):
	def __init__(self, UpdateStatus="Update status missing", TTSEngine = pyttsx3.init(), ComboList = [["hop", 0.5], ["skip", 0.5]], ComboTextSize = 100, Speed = 1):
		tk.Tk.__init__(self)
		self._frame = None
		self.UpdateStatus = UpdateStatus
		#Sets the variables required by the component windows
		self.flag = threading.Event()
		self.TTSEngine = TTSEngine
		self.ComboList = ComboList
		self.ComboTextSize = ComboTextSize
		self.CustomSpeed = Speed
		
		#Opens the StartPage frame first
		self.SwitchFrame(StartPage) #Set the start page

	def SwitchFrame(self, FrameClass):
		#Destroy the current frame, replace with new one. This may cause a memory leak and, as such, should not be used millions of times without restarting the program
		NewFrame = FrameClass(self)
		if self._frame is not None:
			self._frame.destroy()
		self._frame = NewFrame
		self._frame.pack()

class StartPage(tk.Frame):
	#Start page for configuring variables as required
	def __init__(self, master):
		self.master = master
		tk.Frame.__init__(self, master)
		tk.Label(self, text="Welcome to Mantis Combos!", font=("Arial", 20)).pack(side="top", fill="x", pady=10) #Title box
		tk.Label(self).pack(side="top", pady=10)#Blank Space
		
		#The enter box for the speed and the associated content variable
		tk.Label(self, text="Speed:").pack(side="top") #Label for the speed
		self.SpeedBox = tk.Entry(self)
		self.SpeedBox.pack(side="top", pady=10)
		self.SpeedContents = tk.StringVar()
		self.SpeedContents.set(str(master.CustomSpeed))
		self.SpeedBox["textvariable"] = self.SpeedContents
		
		tk.Label(self).pack(side="top", pady=10) #Blank space
		tk.Label(self, text = "Current version: "+Version).pack(side="bottom", fill="x") #Version number, config at the top
		tk.Label(self, text=master.UpdateStatus).pack(side="bottom", fill="x") #Update status, passed through from AppWindow
		tk.Button(self, text="Continue", command= lambda: self.ContinueButton()).pack() #Continue botton to pass into the next 

	def ContinueButton(self):
		#Continue button will set the variables and then open the running page
		InSpeed = ast.literal_eval(self.SpeedContents.get())
		if isinstance(InSpeed, int) or isinstance(InSpeed, float):
			self.master.CustomSpeed = InSpeed
		else:
			self.master.CustomSpeed = 1
		#Opens the running page
		self.master.SwitchFrame(RunningPage)
		

class RunningPage(tk.Frame):
	#A page where, once all else is configured, there are a simple start and stop button to read out the combos
	def __init__(self, master):
		self.master = master
		tk.Frame.__init__(self, master)
		tk.Label(self, text="Ready?").pack(side="top", fill="x", pady=10)
		
		#This label is passed through to the async RunCombos and changed in that context. In practice, the size is set from the preferences csv
		self.current = tk.Label(self, text="Waiting", font=("Arial", master.ComboTextSize), padx = master.ComboTextSize/2, pady = master.ComboTextSize/2)
		self.current.pack(side="top", fill="x", pady=10)
		
		tk.Button(self, text="Quit", bg="#930002",
			command= lambda: self.QuitCombos()).pack(side="bottom")
		
		tk.Button(self, text="Start Combos", bg="#51ae2a",
			command= lambda: self.InitiateCombos()).pack()

	def InitiateCombos(self):
		#Starts the above-defined function to run asynchronously
		self.master.flag.set()
		thr = threading.Thread(target=RunCombos, args=(self.master.TTSEngine, self.master.ComboList, self.master.CustomSpeed, self.current, self.master.flag))
		thr.start()

	def QuitCombos(self):
		#Simple way to stop the async function
		self.master.flag.clear()
		self.master.SwitchFrame(StartPage)


#Debug
if __name__ == "__main__":
	app = AppWindow()
	app.mainloop()