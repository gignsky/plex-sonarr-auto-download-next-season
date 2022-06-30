# Current Version: v0.4.0

# JOIN THE DISCORD FOR THE MOST ACTIVE DISUSSION AND DEVELOPMENT:
https://discord.gg/vSRz2DRGjr

# PURPOSE
PlexSonarrAutoDownloader is a script that connects to Plex and Sonarr to automatically
download the next season of a show you are watching based on the episode you are on.


# VERSION DETAILS

**NOTE**
Python Script will fail to access a users account if a space appears in their name. Should Fix Later.

  # ORIGINAL VERSION v0.1.0
   
   https://github.com/PeacefulDreams/NewEpisodeDownloader
   
    (See. originalScript/docker-PlexSonarrAutoDownloader/)

    -The original version works for the plex server owner account.
    -The script will scan the plex server owner's in-progress tv shows and compare to a list of TV Shows grabbed from Soanrr.
      -If a show has less than the EPISODE_THRESHOLD the script will check to see if a next season exists and if any episodes are already downloaded from that season.
        -If the season exists and no episodes are downloaded the script will send a download command to sonarr.
    -Python build can run automatically with crontab (See. originalScript/crontab - examples.txt)

    **NOTE**
      -If season that download command references is marked as "UNMONITORED" then sonarr will search for the season but fail to send the order to your download client
        -This is one of the issues the a PRODUCTION VERSION aims to fix. (See. production/withMonitorFunction)

  # PRODUCTION VERSIONS | v0.2.0 and Above - Python Only (Might convert to docker eventually)
    (See. production/)

    # NO_MONITOR FUNCTION - VERSION v0.2.0
      (See. noMonitorFunction/)

      -The NO MONITOR VERSION works similarly to the ORIGINAL VERSION in terms of the neccecity for sonarr to already be monitoring both the show and season that the script will inevitablly call upon.
      -This version however has the ability to handle more user accounts than just the server owner.

    # WITH_MONITOR_FUNCTION - VERSION v0.3.0
      (See. withMonitorFunction/)

      -The WITH MONITOR VERSION works similarly to the NO MONITOR VERSION with the added addition that it does not require that you keep your sonarr configured to have undownloaded seasons monitored
        -This version will automatically set the season that it decides to download to monitored prior to downloading thereby leading to a seemless experince when run via crontab periodically.

    -The PRODUCTION VERSIONS have two variations each.
      1. Manual - Intended to be run manually and allows the user to select which user they wish to apply the script to; this can be any user with access to the configured Plex server.
        (See. "manualUserSelectionAutoDownload.py" OR "noMonitor_manualUserSelectionAutoDownload.py" depending on selected usecase)
      2. Automatic - Intended to be run either manually or with a crontab job for automatic processing.
        (See. "noMonitor_PlexSonarrAutoDownloader.py" OR "PlexSonarrAutoDownloader.py" depending on selected usecase)


**********NOTE the monitored scripts have the capablitiy to ensure an entire series is monitored, this is deliberitly turned off by default to avoid acceidently messing up special cases in my test enviroment that might effect yours as well. If you wish to "re-enable" this ability navigate to production/withMonitorFunction/monitorFunctions/monitorMaster.py and undo the large block comment referencing this subject.



# INSTALLATION & CONFIGURATION
  -The script can be installed in two ways: Via Docker or just as a plain Python script with cron.

  Docker install:
  1. cd into the folder of the script.
    (See. originalScript/)
      ***NOTE*** Only the ORIGINAL VERSION has a Docker build at the moment, the PRODUCTION VERSIONS may be updated for a docker image at some point in the future.
  2. Open the script and adjust the variables to your setup (Plex URL, Token, Sonarr URL, Token)
  3. In a terminal, type docker build . to build the docker container. At the end of the process, Docker will tell you the tag
    it has given to the resulting image.
  4. In the same terminal, type docker run [NAME OF CONTAINER IMAGE HERE]
    *(without [])

  Python install
  1. Copy the script version you have decided to run anywhere you like. Be aware that their might be some permission issues with cron depending on where you put it.
  2. Open the script and adjust the variables to your setup (See. config.py in root project directory)
  3. Note that different versions have different python dependencies, (See. "requiredDependancies.txt") for a single line that you can run to install required dependencies based on selected versions.
  4. In a terminal, type crontab -e to add the script to cron and run it periodically
    (See. "crontab - examples.txt")
      - Do however check if the path to your python executable is the same. You can do so by typing 'which python' or 'which python3' in a terminal.
      - Make note of the "script_output.txt" path, this will be the most recent output of the script.


# TESTED ON

  # ORIGINAL VERSION v0.1.0
    The original script was tested on a local environment with two active plex users, so your mileage may vary on larger installs.

  # PRODUCTION VERSIONS v0.2.0 and Above
    Both of the below versions were tested on a LAN enviroment with access available from the outside WAN. 11 total user accounts, 10 of which have consumed some content, but some are MOVIE ONLY watchers and have no interest in television, the script can handle all these exceptions that occur when an account has no in-progress TV Shows.
