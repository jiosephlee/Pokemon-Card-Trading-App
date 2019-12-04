install:
	pip install --upgrade pip
	pip install wheel
	pip install --upgrade pip wheel
	pip install -r doc/requirements.txt

install-1:
	pip3 install --upgrade pip
	pip3 install wheel
	pip3 install --upgrade pip wheel
	pip3 install -r doc/requirements.txt
run:
	python3 run.py

sqlite:
	sqlite3 database.db
