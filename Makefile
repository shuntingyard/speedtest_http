# use make for rapid development cycles
#
all: run

.PHONY: clean venv run test sdist

clean:
	rm -rf src/*.egg-info && rm -rf dist && rm -rf *.log*
	@find . -name __pycache__ -exec rm -rf {} \;

venv:
	venv/bin/python setup.py develop

run: venv
	TZ=Europe/Zurich \
	INFILE=/data/speedtest.csv \
	LOGDIR=. \
	SITENAME="Test uplink" \
	FLASK_APP=speedtest_http FLASK_DEBUG=1 venv/bin/flask run

test: venv
	venv/bin/python -m unittest discover -s tests

sdist: venv test
	venv/bin/python setup.py sdist
