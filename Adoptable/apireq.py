#Request from API, store in database

from lxml import etree
import requests
import mysql.connector
from pet import pet

#Request function
def apiReq(offset):
	
	#Offset to send to API to get new dogs
	currentOffset = offset;

	#Static parameters
	parameters = {'key' : '85425bf687c21951dd70f5de30c4ce6a',
				  'animal' : 'dog',
				  'count' : '1000',
				  'location' : "New York City, New York",
				  'offset' : ''}
	parameters['offset'] = currentOffset

	#Store API request
	dogReqList = requests.get('http://api.petfinder.com/pet.find', params = parameters)

	#Return response object
	return dogReqList


#Initialize current offset
currentOffset = 0

#Initialize counter
numRequests = 0


#Loop that terminates when request per day limit is reached (10,000)
while (numRequests < 1):
	
	#Set dogReqList to api response object
	dogReqList = apiReq(currentOffset)

	#Transform response object to element tree
	root = etree.fromstring(dogReqList.content)

	#Declare list for pet objects
	fullPetList = []

	#Create list of pet objects
	for count in range(1000):
		x = pet()
		fullPetList.append(x)
	
	#Counter for object list
	j = 0

	#Add desired attributes to class instances
	for child in root.iter():
		if (child.tag == 'id'):
			fullPetList[j].id = child.text
		elif (child.tag == 'code'):
			fullPetList[j].code = child.text
		elif (child.tag == 'mix'):
			fullPetList[j].mix = child.text
		elif (child.tag == 'breed'):
			fullPetList[j].breed.append(child.text)
		elif (child.tag == 'animal'):
			fullPetList[j].animal = child.text
		elif (child.tag == 'age'):
			fullPetList[j].age = child.text
		elif (child.tag == 'sex'):
			fullPetList[j].sex = child.text
		elif (child.tag == 'size'):
			fullPetList[j].size = child.text
		elif (child.tag == 'option'):
			fullPetList[j].option.append(child.text)
		elif (child.tag == 'status'):
			if (child.text != '\n'):
				fullPetList[j].status = child.text
		elif (child.tag == 'city'):
			fullPetList[j].city = child.text
		elif (child.tag == 'state'):
			fullPetList[j].state = child.text
		elif (child.tag == 'zip'):
			fullPetList[j].zip = child.text
		elif (child.tag == 'lastOffset'):
			currentOffset = int(child.text)
			print currentOffset
		elif (child.tag == 'phone'):
			j = j +1
			continue
	
	#Update counter
	numRequests = numRequests + 1
	count = 0
	#Update petclass variable totalIDList to be current
	fullPetList[0].getIDList()
	fullPetList[0].randDateGenerate()

	#Loop through list of pet objects, if the id in the object is in the
	#totalIDList then update. If not, then insert
	for i in fullPetList:
		if (fullPetList[0].code != '100'):
			print ('Error!', fullPetList[0].code)
			numRequests = 10000
			break
		else:	
			if (int(i.id) in fullPetList[0].totalIDList):
				i.update()
			else:
				i.inputToDatabase()



