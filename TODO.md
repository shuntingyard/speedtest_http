# TODO list

- [x] Find a method to do *continuous* builds with docker-compose

- [x] Fix instruction in https://github.com/shuntingyard/speedtest_http#dockerhub

- [x] Write a *short*, dockerhub-specific README.md

- [x] Observe (and maybe fix) /lineplot_today, as it continues (for how many
  hours into the night?) showing the last day after midnight.

- [x] Set up Travis.

- [x] Assure this runs on all targeted 3.x versions.

- [x] Review/ complete test cases.

- [ ] Check, complete, comment (README.rst) example startup scripts.

- [ ] Heatmap: hover texts should include hour

- [ ] ver 0.0.5 lab: 3d graph daily download densities for timeframe

- [ ] ver 0.0.6 heatmap etc: see what we gain with a second Reader instance
  not containing "Upload". (Needs fix on `to_Mbit` decorator!)

- [ ] Terminology cleanup in doc and docstrings.

- [ ] Reduce *image size* (python:3.7 alone is > 900MB). If falling back to
  python:3.7-slim, a build toolchain for regex package would be required.

- [ ] Introduce speedtest_lab style comparisons with 2nd sensor
