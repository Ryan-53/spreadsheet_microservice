"""
Name: test_db_select.py
Purpose: select() unit tests
  Tests finding cells in both dbs
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