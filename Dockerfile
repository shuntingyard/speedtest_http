FROM python:3.7
MAINTAINER Tobias Frei (shuntingyard@gmail.com)

# Set /app as working directory.
# WORKDIR /app

# Copy requirements to /app directory.
# COPY requirements.txt /app

# Install required packages.
# RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install --trusted-host pypi.python.org speedtest-http==0.0.2

# Create directories for data access and logging.
RUN \
    mkdir /data \
    mkdir -p /var/log

# Timezone for app AND containers.
ENV TZ UTC

# Configure application environment.
ENV INFILE /data/speedtest.csv
ENV LOGDIR /var/log
ENV SITENAME <Your Sitename here>

# Configure Flask environment.
ENV FLASK_APP speedtest_http
ENV FLASK_DEBUG 0

# Run the app when the container launches.
CMD ["python", "-m", "flask", "run", "-h", "0.0.0.0"]
# , "-p", "8050"]
