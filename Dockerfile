FROM python:3.6
MAINTAINER Tobias Frei (shuntingyard@gmail.com)

# Set build directory.
WORKDIR /build

# Copy project environment.
COPY . /build/

RUN python setup.py install

# Remove project environment.
WORKDIR /
RUN rm -rf /build

# Create directories for data access and logging.
RUN mkdir -p /var/lib/speedtest

# Timezone for app AND containers.
ENV TZ UTC

# Configure application environment.
ENV INFILE /var/lib/speedtest/speedtest.csv
ENV LOGDIR /var/lib/speedtest
ENV SITENAME <Your Sitename here>

# Configure Flask environment.
ENV FLASK_APP speedtest_http
ENV FLASK_DEBUG 0

# Run the app when the container launches.
CMD ["python", "-m", "flask", "run", "-h", "0.0.0.0"]
# , "-p", "8050"]
