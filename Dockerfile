FROM deltaio/delta-docker:0.8.1_2.3.0
# https://github.com/delta-io/delta-docs/blob/main/static/quickstart_docker/0.8.1_2.3.0/Dockerfile

USER root

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY setup.sh /usr/src/app/setup.sh
RUN chmod +x /usr/src/app/setup.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run cron
ENTRYPOINT ["/usr/src/app/setup.sh"]