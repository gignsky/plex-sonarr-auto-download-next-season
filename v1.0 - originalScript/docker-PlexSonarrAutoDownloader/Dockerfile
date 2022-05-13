FROM python:3.7
RUN apt-get update && apt-get -y install cron vim
RUN pip3 install requests plexapi
WORKDIR /app
COPY crontab /etc/cron.d/crontab
COPY PlexSonarrAutoDownloader.py /app/PlexSonarrAutoDownloader.py
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]


