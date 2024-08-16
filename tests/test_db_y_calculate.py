"""
Name: test_db_remove.py
Purpose: calculate() unit tests
  Tests calculating value of cells in both dbs
"""

import os
import db

try:
	FBASE = os.environ["FBASE"]
except:
	FBASE = "0"

FB_URL = "https://" + FBASE + "-default-rtdb.europe-west1.firebasedatabase.app/"

local = "cells.db"
remote = "firebase"


### LOCAL DB TESTS ###

def test_local_calculate_numbers() -> None:
	"""
	Tests calculating 2 numbers on local DB
	"""

	updated = db.insert(local, "C1", 10 + 2)

	assert db.calculate(local, "C1") == '12'

def test_local_calculate_cell() -> None:
	"""
	Tests calculating a number of a cell on local DB
	"""

	updated = db.insert(local, "C2", "B2")

	assert db.calculate(local, "C2") == '4'

def test_local_calculate_both_cells() -> None:
	"""
	Tests calculating 2 cells on local DB
	"""

	updated = db.insert(local, "C3", "B2 + C1")

	assert db.calculate(local, "C3") == '16'
	

def test_local_calculate_cell_link() -> None:
	"""
	Tests calculating cells with one cell having a formula of another cell on 
	local DB
	"""

	updated = db.insert(local, "C4", "C1 + C2 + C3")

	assert db.calculate(local, "C4") == '32'
	

def test_local_calculate_number() -> None:
	"""
	Tests calculating a cell with just a number on local DB
	"""

	cells = ["C1", "C2", "C3", "C4"]

	# Loops through cells created for calculation testing to delete them
	for i in range(len(cells)):
		deleted = db.remove(local, cells[i])

	assert db.calculate(local, "B2") == '4'


### REMOTE DB TESTS ###

def test_remote_calculate_cell() -> None:
	"""
	Tests calculating a number of a cell on remote DB
	"""

	updated = db.insert(remote, "C2", "B2")

	assert db.calculate(remote, "C2") == '4'
	

def test_remote_calculate_number() -> None:
	"""
	Tests calculating a cell with just a number on remote DB
	"""

	cells = ["C1", "C2", "C3", "C4"]

	# Loops through cells created for calculation testing to delete them
	for i in range(len(cells)):
		deleted = db.remove(remote, cells[i])

	assert db.calculate(remote, "B2") == '4'