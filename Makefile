install:
	pip install --upgrade pip
	pip install wheel
	pip install -r doc/requirements.txt
run:
	python3 run.py

sqlite:
	sqlite3 database.db
