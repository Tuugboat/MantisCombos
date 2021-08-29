import csv, os

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

		for C in Combos:
			if (len(C) != 2) or not (isinstance(C[0], str)) or not (isinstance(C[1], float)):
				print("There is an issue with the following combo: "+C)
	return(Combos)