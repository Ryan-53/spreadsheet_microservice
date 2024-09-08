"""
Name: test_db_createtable.py
Purpose: createTable() unit tests
  Tests creation of tables in both dbs
"""

import os
import db

local = "cells.db"
remote = "firebase"

""" createTable() unit tests:
Tests creation of tables in both dbs """

### LOCAL DB TESTS ###

def test_local_createTable() -> None:
  """
  Tests creation of local database
  """

  assert db.createTable(local) == 200

def test_local_createTable_duplicate() -> None:
  """
  Tests creation of local database
  """

  assert db.createTable(local) == 200

def test_createTable_error() -> None:
  """
  Tests attempted creation of non-viable db name
  """

  assert db.createTable("error.db") == 400


### REMOTE DB TESTS ###

def test_remote_createTable() -> None:
  """
  Tests creation of remote database
  """

  assert db.createTable(remote) == 200

def test_remote_createTable_duplicate() -> None:
  """
  Tests creation of remote database
  """

  assert db.createTable(remote) == 200



""" insert() unit tests:
Tests inserting cells in both dbs """

### LOCAL DB TESTS ###

def test_local_insert_standard() -> None:
  """
  Tests inserting a standard value into a new cell in local DB
  """

  assert not db.insert(local, "B2", "6")

def test_local_insert_standard_duplicate() -> None:
  """
  Tests inserting a standard value into the same cell in local DB
  """

  assert db.insert(local, "B2", "4")

### REMOTE DB TESTS ###

def test_remote_insert_standard() -> None:
  """
  Tests inserting a standard value into a new cell in remote DB
  """

  assert not db.insert(remote, "B2", "6")

def test_remote_insert_standard_duplicate() -> None:
  """
  Tests inserting a standard value into the same cell in remote DB
  """

  assert db.insert(remote, "B2", "4")



""" remove() unit tests:
  Tests deleting/clearing value of cells in both dbs """

### LOCAL DB TESTS ###

### LOCAL DB TESTS ###

def test_local_remove_exists() -> None:
  """
  Tests removing an existing cell in local DB
  """
  
  updated = db.insert(local, "X1", "20")
	
  assert db.remove(local, "X1")

def test_local_remove_exists() -> None:
  """
  Tests removing an empty cell in local DB
  """
  
  assert not db.remove(local, "X2")

### REMOTE DB TESTS ###

def test_remote_remove_exists() -> None:
  """
  Tests removing an existing cell in remote DB
  """
  
  updated = db.insert(remote, "X1", "20")
	
  assert db.remove(remote, "X1")

def test_remote_remove_exists() -> None:
  """
  Tests removing an empty cell in remote DB
  """
  
  assert not db.remove(remote, "X2")



""" select() unit tests:
  Tests finding cells in both dbs """

### LOCAL DB TESTS ###

def test_local_select_standard() -> None:
  """
  Tests finding a standard cell in local DB
  """
  
  assert db.select(local, "B2") == {"id":"B2","formula":"4"}

def test_local_select_long() -> None:
  """
  Tests finding a long cell in local DB
  """
  
  updated = db.insert(local, "D1", "99999")

  assert db.select(local, "D1") == {"id":"D1","formula":"99999"}

def test_local_select_formula() -> None:
  """
  Tests finding a formula cell in local DB
  """
  
  updated = db.insert(local, "A1", "3 + 4")

  assert db.select(local, "A1") == {"id":"A1","formula":"7"}

def test_local_select_empty() -> None:
  """
  Tests finding an empty cell in local DB
  """

  deleted = db.remove(local, "A1")
  
  assert db.select(local, "Z1") == None

### REMOTE DB TESTS ###

def test_remote_select_standard() -> None:
  """
  Tests finding a standard cell in remote DB
  """
  
  assert db.select(remote, "B2") == {"id":"B2","formula":"4"}

def test_remote_select_long() -> None:
  """
  Tests finding a long cell in remote DB
  """
  
  updated = db.insert(remote, "D1", "99999")

  assert db.select(remote, "D1") == {"id":"D1","formula":"99999"}

def test_remote_select_formula() -> None:
  """
  Tests finding a formula cell in remote DB
  """
  
  updated = db.insert(remote, "A1", "3 + 4")

  assert db.select(remote, "A1") == {"id":"A1","formula":"7"}

def test_remote_select_empty() -> None:
  """
  Tests finding an empty cell in remote DB
  """

  deleted = db.remove(remote, "A1")
  
  assert db.select(remote, "Z1") == None



""" calculate() unit tests:
  Tests calculating value of cells in both dbs """



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
    


""" listAll() unit tests
  Tests displaying all cells in both dbs """

### LOCAL DB TESTS ###

def test_local_listAll_blank() -> None:
  """
	Tests when an empty space has been left as the cell id on local DB
	"""

  db.insert(local, "", "2")
	
  assert db.listAll(local) == "['', 'B2', 'D1']"
	
def test_local_listAll_standard() -> None:
  """
	Tests during standard usage on local DB
	"""

  deleted = db.remove(local, "")
	
  assert db.listAll(local) == "['B2', 'D1']"

### REMOTE DB TESTS ###
	
def test_remote_listAll_standard() -> None:
  """
	Tests during standard usage on remote DB
	"""
	
  assert db.listAll(remote) == "['B2', 'D1']"



""" dbEmpty() unit tests:
  Tests checking of existence of any cells in both dbs """

### LOCAL DB TESTS ###

def test_local_dbEmpty_full() -> None:
  """
  Tests checking populated DB in local DB
  """
  
  assert not db.dbEmpty(local)

def test_local_dbEmpty_empty() -> None:
  """
  Tests checking empty DB in local DB
  """
  
  deleted = db.remove(local, "B2")
  deleted = db.remove(local, "D1")

  assert db.dbEmpty(local)

### REMOTE DB TESTS ###

def test_remote_dbEmpty_full() -> None:
  """
  Tests checking populated DB in remote DB
  """
  
  assert not db.dbEmpty(remote)

def test_remote_dbEmpty_empty() -> None:
  """
  Tests checking empty DB in remote DB
  """
  
  deleted = db.remove(remote, "B2")
  deleted = db.remove(remote, "D1")

  assert not db.dbEmpty(remote)