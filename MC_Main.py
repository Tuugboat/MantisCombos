import pyttsx3
from time import sleep
from random import randint
import MC_Lib
import csv
import ast

#Initialize the speech engine
SpeechEngine = pyttsx3.init()

#------------------------------- Preferences --------------------------------------
#The following preferences are accepted
#Text to Speech: rate is the speech rate, voice is the system voice (these are configured according to your os)
#Combos: ComboPath will allow you to load external csv files and use those, ComboSpeed is a multiplier applied to the wait time for each combo

Prefs = {}
with open("./Preferences.csv") as file:
	PrefProxy = csv.reader(file)
	for row in PrefProxy:
		Prefs[row[0]] = (ast.literal_eval(row[1]))

SpeechEngine.setProperty("rate", Prefs["rate"])
if Prefs["voice"] != 0:
	SpeechEngine.setProperty("rate", Prefs["voice"])

#Set Other Parameters
if Prefs["ComboPath"] != 0:
	Combos = MC_Lib.GetCombos(Prefs["ComboPath"])
else:
	Combos = MC_Lib.GetCombos()

Speed = Prefs["ComboSpeed"]

del(Prefs)
#------------------------------- Preferences --------------------------------------
IterMax = 5
i=0
while i < IterMax:
	Selection = randint(0, len(Combos)-1)
	SpeechEngine.say(Combos[Selection][0])
	SpeechEngine.runAndWait()
	sleep(Combos[Selection][1]*Speed)
	i+=1