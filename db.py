"""
Name: db.py
Purpose: Handles database calculations, queries and commands
"""

import sqlite3
import os
import requests
import json

try:
	FBASE = os.environ["FBASE"]
except:
	FBASE = "0"

FB_URL = "https://" + FBASE + "-default-rtdb.europe-west1.firebasedatabase.app/"

def createTable(database):
	"""
	Creates a table in the specified DB if it doesn't already exist

	:param database: type of database to created (local or firebase/remote)
	:return: int - response code of the creation of the table
	"""

	# If the local DB is being used
	if database == "cells.db":

		# SQL statement that creates the table if it doesn't already exist
		with sqlite3.connect(database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				"CREATE TABLE IF NOT EXISTS spreadsheet" +
				"(id TEXT PRIMARY KEY, formula TEXT)"
			)
			connection.commit()

		return 200
	
	# If the remote firebase DB is being used
	elif database == "firebase":
		# Checks if the table already exists
		oldSpreadsheet = requests.get(FB_URL + "spreadsheet.json")

		#print(response.status_code)
		
		# If the table does not already exist, create one
		if oldSpreadsheet.status_code == 404:
			newSpreadsheet = requests.put(FB_URL + "spreadsheet.json")

			# New table created
			if newSpreadsheet.status_code == 200:
				print("New table created")
				return 201
			
			# New table not created
			else:
				return 500

		# If the table 
		elif oldSpreadsheet.status_code == 200:
			print("Table already exists")
			return 200
		
		# If it could not connect to remote DB
		else:
			return 404

	# If database variable passed is erroneous, output error message
	else:
		print("ERROR: DB not created")
		return 400


def insert(database, cellId, formula):
	"""
	Adds a cell if it isn't already in the database, otherwise it updates
	a cell already in it.

	:param database: database to access
	:param cellId: PK of cell to add/update to
	:param formula: formula to assign to the cell
	:return: boolean - True if existing cell updated, False if new cell
		created
	"""	

	# If using the local DB
	if database == "cells.db":

		# If the item is already in the database, update it
		if select(database, cellId) != None:	
			with sqlite3.connect(database) as connection:
				cursor = connection.cursor()
				cursor.execute(
					"UPDATE spreadsheet SET formula=? WHERE id=?",
					(formula, cellId)
				)
				connection.commit()
		
			# Return True to signify an existing cell has been updated
			return True

		# If the item is not already in the database, create a new item
		else:
			with sqlite3.connect(database) as connection:
				cursor = connection.cursor()
				cursor.execute(
					"INSERT INTO spreadsheet (id, formula) VALUES(?,?)",
					(cellId, formula)
				)
				connection.commit()

			# Return False to signify a new cell has been created
			return False

	
	# If the remote firebase DB is being used
	else:

		# Creates the path of where the cell is/will be located
		cellPath = "spreadsheet/" + cellId
		
		# Puts properies of cell in a dictionary
		cell = {
			'id':cellId,
			'formula':formula
		}
		
		# Checks if the cell is already in the DB
		oldCell = requests.get(FB_URL + cellPath + ".json")	
			
		# Update/Create the cell with a PUT request
		requests.put(FB_URL + cellPath + ".json", data=json.dumps(cell))

		# If the cell does exist, return True to signify the cell being
		# updated
		if oldCell.status_code == 200 and oldCell.json() is not None:
			return True

		# If the cell does not exist, return False to signify the cell
		# being created
		else:
			return False

def select(database, cellId):
	"""
	Finds a cell and its formula from the database

	:param database: database to access
	:param cellId: PK of item to find
	:return: json object containing the id and formula of the cell
	"""

	# If using the local DB
	if database == "cells.db":

		with sqlite3.connect(database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				"SELECT id, formula FROM spreadsheet WHERE id=?",
				(cellId,)
			)

			cellProp = cursor.fetchone()
	
			# If the cell exists in the DB
			if cellProp:
				# Calculates result of the formula
				calculated = str(calculate(database, cellProp[1]))

				# Returns the json object containing the id and
				# calculated formula value
				return {"id":cellProp[0],"formula":calculated}

			else:
				# Returns None if the cell does not exist
				return None

	# If the remote firebase DB is being used
	else:

		# Creates the path of where the cell should be located
		cellPath = "spreadsheet/" + cellId
		
		# Requests the cell from the DB
		reqCell = requests.get(FB_URL + cellPath + ".json")

		# If the cell exists in the DB
		if reqCell.status_code == 200 and reqCell.json is not None:
		
			# Extracts json file from request to DB
			reqCellJson = reqCell.json()

			# If the json file is not empty
			if reqCellJson is not None:

				# Extracts the id and formula from the json file
				reqCellId = reqCellJson.get("id")
				reqCellFormula = reqCellJson.get("formula")

				# Calculates result of formula
				calculated = str(calculate(database, reqCellFormula))

				# Returns json object containing id and calculated
				# formula value
				return {"id":reqCellId,"formula":calculated}

			# If the json file is empty
			else:
				# Returns None if the json is empty (cell does 
				# not exist)
				return None

		# Returns None if the cell does not exist
		else:	
			return None	
		

def remove(database, cellId):
	"""
	Removes a cell from the database

	:param database: database to access
	:param cellId: PK of DB item to delete
	:return: boolean - True if item deleted, False if not found
	"""

	# If using the local DB
	if database == "cells.db":

		# Checks whether the cell is in the database
		if select(database, cellId) != None:

			# SQL statement to delete a specific cell from the DB
			with sqlite3.connect(database) as connection:
				cursor = connection.cursor()
				cursor.execute(
					"DELETE FROM spreadsheet WHERE id=?",
					(cellId,)
				)
				connection.commit()
		
			# Returns True if the cell has been deleted
			return True

		else:
			# Returns False if the cell could not be found
			return False
	
	# If the remote firebase DB is being used
	else:

		# Creates the path of where the cell should be located
		cellPath = "spreadsheet/" + cellId
	
		# Checks if the cell is already in the DB
		oldCell = requests.get(FB_URL + cellPath + ".json")	
		
		# Deletes cell with given cellId
		delCell = requests.delete(FB_URL + cellPath + ".json")

		# If the cell existed in the DB and has now been deleted
		if delCell.status_code == 200 and oldCell.status_code == 200 and oldCell.json() is not None:

			# Returns True as the cell has been deleted
			return True

		# If the cell could not be found
		else:

			# Returns False as the cell could not be found
			return False
		

def listAll(database):	
	"""
	Lists id's of all cells in the database

	:param database: database to access
	:return: list of the id of every cell in the database
	"""

	# If using the local DB
	if database == "cells.db":

		# Checks if there are no items in the DB
		if not dbEmpty(database):
	
			# SQL statement to output all id's of items in the DB
			with sqlite3.connect(database) as connection:
				cursor = connection.cursor()
				cursor.execute(
					"SELECT id FROM spreadsheet ORDER BY id ASC;"
				)

				# Converts tuple from DB into a list and then turns that
				# into a literal string
				cellProp = cursor.fetchall()
				cellList = list(cellProp)

				# Fomats list to get rid of brackets and extra comma
				for i in range(len(cellList)):
					cellList[i] = str(cellList[i]).strip("()',")

				# Converts list of cell ids into a string so it can be
				# returned
				cellString = str(cellList)
			
				# Returns a list of all ids in DB
				return cellString

		# Returns an empty list if there are no cells in the DB
		else:
			return "[]"

	# If the remote firebase DB is being used
	else:

		# Creates the path of where the cell should be located
		cellPath = "spreadsheet"
		
		# Checks if the cell is already in the DB
		cells = requests.get(FB_URL + cellPath + ".json")
		cellsJson = cells.json()

		# If the cell exists in the DB
		if cells.status_code == 200 and cellsJson is not None:

			# Extract PKs (ids) from the cells JSON
			ids = cellsJson.keys()

			# Converts ids into a list then into a string
			listIds = list(ids)
			stringIds = str(listIds)

			return stringIds

		# Returns an empty list if there are no cells in the DB
		else:
			return "[]"


def calculate(database, formula):
	"""
	Calculates result of a cell's formula

	:param database: database to access
	:param formula: formula of cell to calculate
	:return: calculated value of cell
	"""

	# Splits formula by spaces
	formulaValues = formula.split() 

	# If there is only 1 value in the formula (i.e. no calculation)
	if len(formulaValues) == 1:
		# If the value is a number, return that number
		if formula.isnumeric():
			return formula
		# If the value references another cell, return the formula of
		# that cell
		else:

			# Reads the formula of the referenced cell
			calculatedJson = select(database, formula)

			# If the referenced cell is not empty (does not exist)
			if calculatedJson is not None:

				# Returns formula of referenced cell - this
				# will also be fully evaluated already
				return calculatedJson.get("formula")

			# If the referenced cell is empty, treat it as a value
			# of zero
			else:
				return 0

	# If there are multiple values in the formula (a calculation takes
	# place
	else:

		# Loops for all values of the list, getting the values of any
		# cells referenced
		for i in range(len(formulaValues)):

			# Checks if the value in the list index is not a number
			if not formulaValues[i].isnumeric():

				# Checks if the value in the list index is not
				# an operator
				if len(formulaValues[i]) > 1:
					
					# Reads the formula of the referenced
					# cell
					numberValueJson = select(database, formulaValues[i])

					# If the referenced cell is not empty (does not exist)
					if numberValueJson is not None:

						# Overwrites value of formula of referenced 
						# cell into this cells formula- this will
						# also be fully evaluated already
						formulaValues[i] = numberValueJson.get("formula")

					# If the referenced cell is empty, treat it as a value
					# of zero
					else:
						return 0
					
		# Joins all items in the list into a string
		formulaStr = ' '.join(formulaValues)

		# Evaluates formula as string, producing a numeric result
		return eval(formulaStr)
			
def dbEmpty(database):
	"""
	Checks whether the database is empty

	:param database: database to access
	:return: boolean - True if the database is empty, False if not
	"""

	if database == "cells.db":

		# SQL statement to output the number of items in the DB
		with sqlite3.connect(database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				"SELECT COUNT(*) FROM spreadsheet"	
			)

			# 
			cellProp = cursor.fetchone()
			
			# If the count of number of items in the DB is 0 return True.
			# Indicates an empty DB
			if cellProp[0] == 0:
				return True

			# Otherwise, return False, indicating a populated DB
			else:
				return False
	
	else:
		return False