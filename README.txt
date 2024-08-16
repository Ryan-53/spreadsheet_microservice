Flask Microservice providing the backend of a spreadsheet

Can use a local DB (sqlite) or remote (firebase, API key required)

----------------------------

To launch:

local DB:
  python sc.py -r sqlite

or

remote DB:
  python sc.py -r firebase

----------------------------

Hosted on:

localhost:3000

Interaction via curl commands

e.g. Creating a cell(B2) with formula(6):

curl -s -X PUT -d "{\"id\":\"B2",\"formula\":\"6"}" \
  -H "Content-Type: application/json" -w "%{http_code}" \
  localhost:3000/cells/B2

e.g. Reading the cell(B2):

curl -s -X GET -o body -w "%{http_code}" localhost:3000/cells/B2

----------------------------

Run unit testing:

python -m pytest