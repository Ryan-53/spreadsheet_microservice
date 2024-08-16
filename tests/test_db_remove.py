"""
Name: test_db_remove.py
Purpose: remove() unit tests
  Tests deleting/clearing value of cells in both dbs
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

