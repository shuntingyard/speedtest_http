#!/bin/sh

# Run the container:

# Except for UTC, TZ should always be set for app AND containers.
sudo docker run \
    --restart always \
    --publish 80:5000 \
    --volume /data:/var/lib/speedtest \
    --env "TZ=Europe/Zurich" \
    --env "SITENAME=Uplink green.ch" \
    --tty --interactive \
    shuntingyard/speedtest_http

    # On CentOS 7:
    #
    # - logging to /data/log, which now has pol label svirt_sandbox_file_t .
    #
    # - SELinux net essentials - for listing objects e.g.
    #
    #       # semanage port -l | grep -w http_port_t
    #   or
    #       # sepolicy network -p 8001
    #

    #
    # Using nginx as a reverse proxy with al little help from
    #
    #   https://www.sam.today/blog/stop-disabling-selinux:-a-real-world-guide/
    #
