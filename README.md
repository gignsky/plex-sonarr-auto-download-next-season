# PURPOSE
PlexSonarrAutoDownloader is a script that connects to Plex and Sonarr to automatically
download the next season of a show you are watching based on the episode you are on.

# VERSION DETAILS
**NOTE**
Python Script will fail to access a users account if a space appears in their name. Should Fix Later.

  # ORIGINAL VERSION
    (See. originalScript/docker-PlexSonarrAutoDownloader/)

    -The original version works for the plex server owner account.
    -The script will scan the plex server owner's in-progress tv shows and compare to a list of TV Shows grabbed from Soanrr.
      -If a show has less than the EPISODE_THRESHOLD the script will check to see if a next season exists and if any episodes are already downloaded from that season.
        -If the season exists and no episodes are downloaded the script will send a download command to sonarr.
    -Python build can run automatically with crontab (See. originalScript/crontab - examples.txt)

    **NOTE**
      -If season that download command references is marked as "UNMONITORED" then sonarr will search for the season but fail to send the order to your download client
        -This is one of the issues the a PRODUCTION VERSION aims to fix. (See. production/withMonitorFunction)
