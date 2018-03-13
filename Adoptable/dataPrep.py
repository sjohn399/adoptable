#Prepare data for machine learning. Send to csv

from pet import pet
from datetime import date
import pandas as pd
import numpy as np
import mysql.connector

#Create data frame to store features from animal_t
fieldNames = ['small', 'medium', 'large', 'xtraLarge', 'male', 'female', 'mixY', 'mixN', 'baby', 'young', 'adult', 'senior', 'timeToAdoption']
testCases = pd.DataFrame(columns = fieldNames)


#List to include all pets that are training examples and for id comparison
fullPetList  = []

#Create empty list of 1000 mock data. Could get number of valid test cases before hand use this to have
#full list of acceptable training examples
for count in range(1000):
	x = pet()
	fullPetList.append(x)

#Open connection
cnx = mysql.connector.connect(user='root', password = '1269', database='adoptable')
cursor = cnx.cursor()

#Query to put all the data in. CHECK VALIDTC IF THIS EVERY ACTUALLY HAS MEANINGFUL DATA
query = ("SELECT id, size, sex, mix, age, dateAdded, dateAdopt FROM animal_t WHERE validTC = 0")

#Execute query
cursor.execute(query)

#Counter to access objects in fullPetList
counter = 0

for (_id, size, sex, mix, age, dateAdded, dateAdopt) in cursor:
	
	#Calculate days it took to be adopted
	d0 = dateAdopt
	d1 = dateAdded
	delta = d0 - d1
	daysDelta = delta.days


	#Turn categories into numerical data
	#Size
	if (size == 'S'):
		inputSize = [1, 0, 0, 0]
	elif (size == 'M'):
		inputSize = [0, 1, 0, 0]
	elif (size == 'L'):
		inputSize = [0, 0, 1, 0]
	elif (size == 'XL'):
		inputSize = [0, 0, 0, 1]

	#Sex
	if (sex == 'M'):
		inputSex = [1, 0]
	elif (sex == 'F'):
		inputSex = [0, 1]

	#Mix
	if (mix == 'yes'):
		inputMix = [1, 0]
	elif (mix == 'no'):
		inputMix = [0, 1]

	#Age
	if (age == 'Baby'):
		inputAge = [1, 0, 0, 0]
	elif (age == 'Young'):
		inputAge = [0, 1, 0, 0]
	elif (age == 'Adult'):
		inputAge = [0, 0, 1, 0]
	elif (age == 'Senior'):
		inputAge = [0, 0, 0, 1]

	#Add id to pull pet list class iteration for later comparison
	fullPetList[counter].id = _id
	counter += 1
	
	#PLACE FOR TYPE WHEN OTHER ANIMALS ARE INCLUDED

	#Assign 
	tempList = inputSize + inputSex + inputMix + inputAge
	tempList.append(daysDelta)

	testCases.loc[counter] = tempList


#Query for breeds
query = ("SELECT animal_t.id, breed_t.breedName FROM breed_t, animal_t, hasBreed_t WHERE animal_t.id = hasBreed_t.id AND hasBreed_t.breedID = breed_t.breedID ORDER BY animaL_t.id")

#Execute query
cursor.execute(query)

#Counter for fullPetList
counter = 0

#Counter for the breed dataframe
breedCounter = 0

#Get full breed list class list variable
fullPetList[0].updateBreedList()

#Get the columns from the total breedList
breedCols = fullPetList[0].totalBreedList

#There will be as many cells as there are cols.
#Assume none of the dogs qualify as having a breed
#Set all to zero
breedRow = [0] * len(breedCols)

#breed dataframe, columns totalBreedList
breedDF = pd.DataFrame(columns = breedCols)

#There is probably a more efficient way to do this, but I already got in to deep to back track
#mentally. The fullPetList id variable will be in the same ascending order as the breed query
#thus each dog can be checked for its multiple breeds. When the dog changes the else statement
#will trigger, the old dog's breed row will be added to the data frame. The breed row will be reset
#and the new dogs first breed will be added. Counter adjusted appropriately.
for (_id, breedName) in cursor:
	if fullPetList[counter].id == _id:
		index = breedCols.index(breedName)
		breedRow[index] = 1
	else:
		breedDF.loc[breedCounter] = breedRow
		breedRow = [0] * len(breedCols)
		index = breedCols.index(breedName)
		breedRow[index] = 1
		breedCounter += 1
		counter += 1

#Last dog needs their row added
breedDF.loc[breedCounter] = breedRow

#Adjust index so DFs can be murged
breedDF.index = np.arange(1,len(breedDF)+1)

#close cursor
cursor.close()
cnx.close()

#Combine dataframes
totalDF = pd.concat([testCases, breedDF], axis = 1)

#Send to CSV files
totalDF.to_csv('trainingCases.csv')

###### THIS IS THE OPTION DATAFRAME ADDITION. THE DIFFICULTLY IS THAT NOT EVERY XML DATA SHEET 
###### HAD A SET OF OPTIONS. THERE ARE ONLY 950 UNIQUE PET CLASS IDS IN THE HAS_OPTION_T
###### HAVE TO FIGURE OUT HOW TO ADD ROWS OF ALL 0s TO THE ABSENT IDS
###### FOR LATER 

#query = ("SELECT animal_t.id, hasOption_t.optionID FROM option_t, animal_t, hasOption_t WHERE animal_t.id = hasOption_t.id AND hasOption_t.optionID = option_t.optionID ORDER BY animaL_t.id")

#cursor.execute(query)

#counter = 0

#optionCols = ['altered', 'hasShots', 'housetrained', 'noKids', 'noCats', 'noDogs', 'specialNeeds']
#optionDF = pd.DataFrame(columns = optionCols)
#optionRows = [0, 0, 0, 0, 0, 0, 0]

#for (_id) in cursor:
#	if (counter == 1000):
#		break
#	if fullPetList[counter].id == _id:
#		testList.append(_id)
#		if (optionID  == 1):
#			optionRows[0] = 1
#		elif (optionID == 2):
#			optionRows[1] = 1
#		elif (optionID == 3):
#			optionRows[2] = 1
#		elif (optionID == 4):
#			optionRows[3] = 1
#		elif (optionID == 5):
#			optionRows[4] = 1
#		elif (optionID == 6):
#			optionRows[5] = 1
#		elif (optionID == 7):
#			optionRows[6] = 1
#	else:
#		optionDF.loc[counter] = optionRows
#		optionRows = [0, 0, 0, 0, 0 ,0, 0]
#		if (optionID == 1):
#			optionRows[0] = 1
#		elif (optionID == 2):
#			optionRows[1] = 1
#		elif (optionID == 3):
#			optionRows[2] = 1
#		elif (optionID == 4):
#			optionRows[3] = 1
#		elif (optionID == 5):
#			optionRows[4] = 1
#		elif (optionID == 6):
#			optionRows[5] = 1
#		elif (optionID == 7):
#			optionRows[6] = 1
#		counter += 1

#optionDF.loc[counter] = optionRows

###			LOCATION NOT RELEVANT UNTIL I HAVE ACTUAL TEST CASES
####
#query = ("SELECT animal_t.id, zip, cityTown, state FROM location_t, animal_t, hasLocation_t WHERE animal_t.id = hasLocation_t.id AND haslocation_t.locationID = location_t.locationID ORDER BY animaL_t.id")

#cursor.execute(query)

#counter = 0

#for (_id, _zip, cityTown, state) in cursor:
#	fullPetList[counter].zip = _zip
#	fullPetList[counter].city = cityTown
#	fullPetList[counter].state = state
#	counter += 1


#cursor.close()
#cnx.close()