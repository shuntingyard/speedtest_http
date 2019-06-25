# use make for rapid development cycles
#
all: run

.PHONY: clean pull run test sdist

clean:
	rm -rf venv
	rm -rf src/*.egg-info && rm -rf build rm -rf dist && rm -rf *.log*

venv:
	python -m venv venv

pull: venv
	venv/bin/python setup.py install

run: pull
	@TZ=Europe/Zurich \
		INFILE=/data/speedtest.csv \
		LOGDIR=. \
		SITENAME="Test uplink" \
		FLASK_APP=speedtest_http FLASK_DEBUG=1 venv/bin/flask run -h 0.0.0.0

test: pull
	venv/bin/python setup.py test

sdist: test
	venv/bin/python setup.py sdist
