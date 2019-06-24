# use make for rapid development cycles
#
all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

venv:
	python -m venv venv && venv/bin/python setup.py develop
	# python -m venv venv && venv/bin/python setup.py install

run: venv
	# FLASK_APP=speedtest_http SPEEDTEST_HTTP_SETTINGS=../../settings.cfg venv/bin/flask run
	FLASK_APP=speedtest_http FLASK_DEBUG=1 DEBUG=1 venv/bin/flask run

test: venv
	# SPEEDTEST_HTTP_SETTINGS=../../settings.cfg venv/bin/python -m unittest discover -s tests
	venv/bin/python -m unittest discover -s tests

sdist: venv test
	venv/bin/python setup.py sdist
