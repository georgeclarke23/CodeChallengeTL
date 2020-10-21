
-include .env
export


venv:
	python3 -m venv .venv
	. ./.venv/bin/activate &&  make reqs


reqs:
	pip install -r requirements.txt

docker/compose:
	docker-compose up --build

run:
	python3 main.py

docker/run:
	tail -f /dev/null

query:
	python3 query.py "${q}"