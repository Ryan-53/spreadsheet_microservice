"""
Name: sc.py
Purpose: Handles database interactions with user
"""

import sqlite3
from flask import Flask, request
import sys
import db


app = Flask(__name__)

# Takes command line argument of type of db to use, defaults to local
try:
	# Switches between using local and remote db based on command line argument
	storage = sys.argv[2]
except:
	storage = "sqlite"

# If sqlite is the cmd line argument, the local DB is used
if storage == "sqlite":
	database = "cells.db"

# If firebase is cmd line argument, a remote cloud based DB is used
elif storage == "firebase":
	database = "firebase"

# Creates a table in the specified DB if it doesn't already exist
tableCreationCode = db.createTable(database)


@app.route("/cells/<string:cellId>",methods=["PUT"])
def create(cellId):
	"""
	Creates or updates a cell by id with a formula held in a JSON file

	:param cellId: id of cell to create/update
	:return: status code
	"""

	# Gets the JSON object passed in through the PUT command
	js = request.get_json()
	# Gets the value of the formula to be inserted into the cell at cellId
	formula = js.get("formula")
	# Gets the value of the id passed through the JSON object
	jsonId = js.get("id")
	

	# Checks the cellId and formula are not empty values and that the
	# cellId in the json file matches that of the one in the address
	if cellId is not None and cellId == jsonId \
		and formula is not None and len(formula) != 0 and not formula.isspace():

		# Creates/updates a cell with cellId by formula, returning a
		# boolean as to whether the cell was already there
		updated = db.insert(database, cellId, formula)

		# If a current cell was updated
		if updated:
			return "",204 # No Content (cell updated)

		# If a new cell was created
		else:
			return "",201 # OK (cell created)

	# If cellId or formula is an empty value
	else:
		return "",400 # Bad Request


@app.route("/cells/<string:cellId>",methods=["GET"])
def read(cellId):
	"""
	Reads a cell by id 

	:param cellId: id of cell to read
	:return: status code and a JSON object with the contents of the cell
		along with id if it exists in the DB
	"""

	# Gets the JSON object of the cell with id of cellId
	cell = db.select(database, cellId)

	# If the cell is not empty
	if cell != None:
		return cell,200 # OK

	# If the cell is empty
	else:
		return "",404 # Not Found

		
@app.route("/cells/<string:cellId>",methods=["DELETE"])
def delete(cellId):
	"""
	Deletes a cell by id

	:param cellId: id of cell to delete
	:return: status code
	"""

	# Removes the cell if it exists; True or False whether the cell was
	# found or not
	deleted = db.remove(database, cellId)

	# If the cell was found and deleted
	if deleted:
		return "",204 # No Content (cell deleted)

	# If the cell was not found
	else:
		return "",404 # Not found


@app.route("/cells",methods=["GET"])
def list():
	"""
	Lists the id of all the cells currently in the DB

	:return: a list containing all the ids and the status code
	"""

	# Gets the list of every id of all cells currently in the DB
	cells = db.listAll(database)

	# Returns the list of cells as a list as well as a 200 status code
	return cells,200 # OK


if __name__ == "__main__":
	#main()
	app.run(host="localhost",port=3000)
