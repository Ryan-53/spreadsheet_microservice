"""
Name: test_db_listall.py
Purpose: listAll() unit tests
  Tests displaying all cells in both dbs
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