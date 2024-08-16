"""
Name: test_db_insert.py
Purpose: insert() unit tests
  Tests inserting cells in both dbs
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