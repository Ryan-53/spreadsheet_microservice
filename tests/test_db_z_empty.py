"""
Name: test_db_z_empty.py
Purpose: dbEmpty() unit tests
  Tests checking of existence of any cells in both dbs
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