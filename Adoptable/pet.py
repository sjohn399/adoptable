#Pet Class file

import mysql.connector
import datetime
import random
import numpy as np

#Data structure to store individual XML data
class pet():

	totalBreedList = []			#Class variable to hold all of the breeds currently known

	totalOptionList = []		#Class variable to hold all of the options currently known

	totalLocationList = []		#Class variable to hold all of the options currently known

	totalIDList = []			#Class variable to hold all of the ids in the database

	randDateList = []			#Class variable to hold all the mock adopt dates

	globalCounter = 0
	
	#Constructor
	def __init__(self):
		self.id = None
		self.code = None
		self.mix = None
		self.breed = []
		self.animal = None
		self.age = None
		self.size = None
		self.sex = None
		self.option = []
		self.status = None
		self.city = None
		self.state = None
		self.zip = None

	#Generate random adopttion dates for mock data
	def randDateGenerate(self):
		
		date = np.array('2018-05-01', dtype = np.datetime64)

		dateList = date + np.arange(1000)

		for i in dateList:
			myS = str(i)
			self.randDateList.append(myS)
		#while (i < 1000):
		#	year = random.randint(2019,2023)
		#	month = random.randint(1,12)
		#	day = random.randint(1,28)
#
#			adoptionDate = datetime.datetime(year, month, day)
#
#			self.randDateList.append(adoptionDate)
#
#			i = i + 1 


	#Update 
	def update(self):

		#Open connection
		cnx = mysql.connector.connect(user = 'root', password = '1269', database = 'adoptable')
		cursor = cnx.cursor()

		#Find the status value where the id is the same as the id in the current instance
		query = ("SELECT status FROM animal_t "
					 "WHERE id = %s")

		cursor.execute(query, (self.id,))

		databaseStatus = cursor.fetchone()

		databaseStatus = databaseStatus[0]

		#If the database status is different than the current status it means its changed
		#If it has changed, update the status cell
		if (databaseStatus != self.status):
			update_status = ("UPDATE animal_t "
							 "SET status = %s "
							 "WHERE id = %s")
			data_status = (self.status, self.id)

			cursor.execute(update_status, data_status)
			cnx.commit()

		#If the databaseStatus was A, H, or P (up for adoption) and the new status was X (now adopted)
		#then add the dateAdopt date to the dateAdopt cell! Hoila! You have a valid training case
		if ((databaseStatus == 'A' or databaseStatus == 'H' or databaseStatus == 'P') and self.status == 'X'):

			now = datetime.now()

			currentDate = now.strftime("%Y-%m-%d")

			update_dateAdopt = ("UPDATE animal_t "
								"SET dateAdopt = %s"
								"WHERE id = %s")
			data_dateAdopt =  (now, self.id)
			cursor.execute(update_dateAdopt, data_dateAdopt)
			cnx.commit()

		cursor.close()
		cnx.close()


	#Input data into database
	def inputToDatabase(self):

		#Update the breedlist
		self.updateBreedList()

		#Update option list
		self.updateOptionList()

		#Update location list
		self.updateLocationList()

		#Open connection to database
		cnx = mysql.connector.connect(user = 'root', password = '1269', database = 'adoptable')
		cursor = cnx.cursor(buffered =True)

		#PUT THRESHOLD FOR VALIDTC HERE

		#Input data into animal_t
		add_animal = ("INSERT INTO animal_t "
					  "(id, size, status, sex, mix, age, type, dateAdded, validTC, dateAdopt)"
					  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
		
		now = datetime.datetime.now()

		currentDate = now.strftime("%Y-%m-%d")

		data_animal = (self.id, self.size, self.status, self.sex, self.mix, self.age, self.animal, currentDate, 0, self.randDateList[self.globalCounter])

		pet.globalCounter += 1
		
		cursor.execute(add_animal, data_animal)
		cnx.commit()

		#Input data into hasLocation_t

		query = ("SELECT locationID FROM location_t "
				 "WHERE zip = %s")

		cursor.execute(query, (self.zip,))

		currentLocationID = cursor.fetchone()

		currentLocationID = currentLocationID[0]

		add_hasLocation = ("INSERT INTO hasLocation_t "
						"(id, locationID)"
						"VALUES (%s,%s)")

		data_hasLocation = (self.id, currentLocationID)
		cursor.execute(add_hasLocation, data_hasLocation)

		#Loop through the breed list of the specific animal. Retrieve the breedID based on its breedName
		#and add the breedID and the API id to the hasBreed table
		for i in self.breed:
			query = ("SELECT breedID FROM breed_t "
					 "WHERE breedName = %s")

			cursor.execute(query, (i,))

			#Fetonce method returns a tuple, get first element
			currentBreedID = cursor.fetchone()

			#Check for None Type
			if (currentBreedID != None):

				currentBreedID = currentBreedID[0]

				add_hasBreed = ("INSERT INTO hasBreed_t"
							 "(id, breedID)"
							 "VALUES(%s,%s)")
					
				data_hasBreed = (self.id, currentBreedID)

				cursor.execute(add_hasBreed, data_hasBreed)
				cnx.commit()
		
		#Similar procedure to input into hasOption_t
		for i in self.option:
			query = ("SELECT optionID FROM option_t "
					 "WHERE optionName = %s")

			cursor.execute(query, (i,))

			currentOptionID = cursor.fetchone()

			currentOptionID = currentOptionID[0]

			add_hasOption = ("INSERT INTO hasOption_t"
						 "(id, optionID)"
						 "VALUES(%s,%s)")
				
			data_hasOption = (self.id, currentOptionID)

			cursor.execute(add_hasOption, data_hasOption)
			cnx.commit()


		cursor.close()
		cnx.close()

	def updateBreedList(self):

		#Open connection with database
		cnx = mysql.connector.connect(user = 'root', password = '1269', database = 'adoptable')
		
		#Create cursor
		cursor = cnx.cursor()

		#Prepare query for all breed names in breed_t
		query = ("SELECT breedName FROM breed_t")

		#Execute query
		cursor.execute(query)

		#Loop through breednames in cursor. They come out as tuples so access the first element
		#If that element ("Beagle") is not in the totalBreedList, append it to the end of the list
		for (breedName) in cursor:
			temp = breedName[0]
			if (temp not in self.totalBreedList):
				self.totalBreedList.append(temp)

		#Loop through the list of breeds for a particular dog. If the breed is not in the total breed
		#list add the breed to the breed_t table
		for i in self.breed:
			if (i not in self.totalBreedList):
				add_breed = ("INSERT INTO breed_t"
							 "(breedName)"
							 "VALUES(%s)")
				data_breed = i
				cursor.execute(add_breed,(data_breed,))
				cnx.commit()

		cursor.close()
		cnx.close()

	def updateOptionList(self):

		#Open connection with database
		cnx = mysql.connector.connect(user = 'root', password = '1269', database = 'adoptable')
		
		#Create cursor
		cursor = cnx.cursor()

		#Prepare query for all option names in option_t
		query = ("SELECT optionName FROM option_t")

		#Execute query
		cursor.execute(query)

		for (optionName) in cursor:
			temp = optionName[0]
			if (temp not in self.totalOptionList):
				self.totalOptionList.append(temp)

		for i in self.option:
			if (i not in self.totalOptionList):
				add_option = ("INSERT INTO option_t"
							 "(optionName)"
							 "VALUES(%s)")
				data_option = i
				cursor.execute(add_option,(data_option,))
				cnx.commit()

		cursor.close()
		cnx.close()

	def updateLocationList(self):

		#Open connection with database
		cnx = mysql.connector.connect(user = 'root', password = '1269', database = 'adoptable')
		
		#Create cursor
		cursor = cnx.cursor()

		#Get zip codes from location_t
		query = ("SELECT zip FROM location_t")

		#Execute query
		cursor.execute(query)

		#Loop through the cursor. If the zip isn't in the totalLocationList append it to it
		for (myZip) in cursor:
			temp = myZip[0]
			if (temp not in self.totalLocationList):
				self.totalLocationList.append(temp)

		#No need to loop. Each animal only has one location. If the zip isn't in the totalLocationList
		#then add it to location_t along with the cityTown and state
		if (int(self.zip) not in self.totalLocationList):
			add_location = ("INSERT INTO location_t"
						  "(zip, cityTown, state)"
						  "VALUES(%s,%s,%s)")
			data_location = (self.zip, self.city, self.state)
			cursor.execute(add_location, data_location)
			cnx.commit()

		cursor.close()
		cnx.close()

	def getIDList(self):

		#Open connection with database
		cnx = mysql.connector.connect(user = 'root', password = '1269', database = 'adoptable')
		
		#Create cursor
		cursor = cnx.cursor()

		#Get zip codes from location_t
		query = ("SELECT id FROM animal_t")

		#Execute query
		cursor.execute(query)

		#Loop through the cursor. If the zip isn't in the totalLocationList append it to it
		for (myID) in cursor:
			temp = myID[0]
			if (temp not in self.totalIDList):
				self.totalIDList.append(temp)

		cursor.close()
		cnx.close()