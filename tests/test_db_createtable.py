"""
Name: test_db_createtable.py
Purpose: createTable() unit tests
  Tests creation of tables in both dbs
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
