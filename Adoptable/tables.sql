#Build tables for storage

DROP TABLE IF EXISTS hasOption_t;
DROP TABLE IF EXISTS hasBreed_t;
DROP TABLE IF EXISTS hasLocation_t;
DROP TABLE IF EXISTS breed_t;
DROP TABLE IF EXISTS option_t;
DROP TABLE IF EXISTS location_t;
DROP TABLE IF EXISTS animal_t;

CREATE TABLE animal_t
(

	id			INT unsigned NOT NULL, 								#ID from Petfinders API
	size		VARCHAR(2) NOT NULL, 								#Size of animal
	status		VARCHAR(1) NOT NULL, 								#Adoption status
	sex			VARCHAR(1) NOT NULL,								#Male or female
	mix			VARCHAR(3) NOT NULL,								#Is it a mix or not?
	age			VARCHAR(10) NOT NULL,								#Age of animal
	type 	  	VARCHAR(20) NOT NULL,								#Type of animal (dog, cat, pig etc.)
	validTC		BOOLEAN NOT NULL,									#Attribute that determines whether it is a valid test case to use for the ML
	dateAdded	DATE,												#Date added to the database
	dateAdopt	DATE,												#Date adopted 
	CONSTRAINT PK_animal_t PRIMARY KEY (id)
);

CREATE TABLE breed_t
(
	breedID 	INT unsigned NOT NULL AUTO_INCREMENT,				#Unique ID to identify type of breed (Pitbull, Pug, etc.)
	breedName	VARCHAR(40) NOT NULL,								#Breed name (Pitbull, Pug etc.)
	CONSTRAINT PK_breed_t PRIMARY KEY (breedID)
);

CREATE TABLE option_t
(
	optionID	INT unsigned NOT NULL AUTO_INCREMENT,				#ID for each potential option
	optionName	VARCHAR(40) NOT NULL,								#Name of the option (noKids, noDogs etc.)
	CONSTRAINT PK_option_t PRIMARY KEY (optionID)
);

CREATE TABLE location_t
(
	locationID 	INT unsigned NOT NULL AUTO_INCREMENT,				#individual location
	zip			INT unsigned NOT NULL, 								#zip code
	cityTown	VARCHAR(40),		   								#city or town where animal is located
	state		VARCHAR(40)	,		   								#state where animal is located
	CONSTRAINT PK_location_t PRIMARY KEY (locationID)
);

CREATE TABLE hasLocation_t
(
	id 			INT unsigned NOT NULL,								#API ID
	locationID	INT unsigned NOT NULL,								#Zip code of animal
	CONSTRAINT FK_animalHasLocation FOREIGN KEY (id)
	REFERENCES animal_t(id),
	CONSTRAINT FK_locationHasLocation FOREIGN KEY (locationID)
	REFERENCES location_t(locationID)
);

CREATE TABLE hasBreed_t
(
	id 			INT unsigned NOT NULL,								#ID from Petfinders API				
	breedId		INT unsigned NOT NULL, 								#Unique ID to identify type of breed (Pitbull, Pug, etc.)	
	CONSTRAINT FK_animalHasBreed FOREIGN KEY (id)
	REFERENCES animal_t(id),
	CONSTRAINT FK_breedHasBreed FOREIGN KEY (breedID)
	REFERENCES breed_t(breedID)
);

CREATE TABLE hasOption_t
(
	id 			INT unsigned NOT NULL,								#ID from Petfinders API
	optionID	INT unsigned NOT NULL,								#ID for each potential option
	CONSTRAINT FK_animalHasOption FOREIGN KEY(id)
	REFERENCES animal_t(id),
	CONSTRAINT FK_optionHasOption FOREIGN KEY(optionID)
	REFERENCES option_t(optionID)
);

DESCRIBE animal_t;
DESCRIBE hasBreed_t;
DESCRIBE breed_t;
DESCRIBE hasOption_t;
DESCRIBE option_t;
DESCRIBE hasLocation_t;
DESCRIBE location_t;
