# Current Version: v0.5.2

# CURRENT VERSION DETAILS:
    - unified script that combines the old versions into one single script with broken apart modules allowing for easier modification in the future
    - updated readme version number
    - fixed bug in issue #40

# JOIN THE DISCORD FOR THE MOST ACTIVE DISUSSION AND DEVELOPMENT:
https://discord.gg/vSRz2DRGjr

# PURPOSE
Plex-Sonarr-Auto-Downloader is a script that connects to Plex and Sonarr to automatically
download the next season of a show you are watching based on the episode you are on.

# INSTALLATION:
1. Download current zip file from releases
2. Unpack zip file into directory you want to run script from
3. Ensure requred dependencies are installed
    - Check required_dependencies.md
4. Modify Settings
    A. Open "config.py" and modify CONSTANTS under "# START HERE"
        - This includes PLEX_URL, PLEX_TOKEN, SONARR_URL, & SONARR_API_KEY
    B. Open "settings_constants.py" and modify TEST_MODE to "True" (without the quotes) if you wish to run this script in test mode
        - See information in "settings_constants.py" for more information about TEST_MODE
5. RUNNING THE SCRIPT
    A. To run automatically run the file with the argument "auto" (without the quotes) directly after the "main.py"
        - (e.x. python3 main.py auto) | this will run the script in auto mode
    B. To run the script manually run the file without the "auto" argument
        - (e.x. python3 main.py) | this will run the script in manual mode allowing for script allowing for manual selection of which user to monitor
6. Cronjobs | if you want to add a cronjob check "crontab - examples.txt" for instructions

# OPTIONS:
  **NOTE** the monitored scripts have the capablitiy to ensure an entire series is monitored, this is deliberitly turned off by default to avoid acceidently messing up special cases in my test enviroment that might effect yours as well. If you wish to "re-enable" this ability navigate to production/withMonitorFunction/monitorFunctions/monitorMaster.py and undo the large block comment referencing this subject.

# NOTE ON PREVIOUS VERSIONS
- Details pertaining to older versions of the script have been removed from this README.md if you would like to know about the changes please reference the detailed README's in each previous branch pertaining to the version you are curious about.

# KNOWN ISSUES:
- [Ref. #34] Python Script will fail to access a users account if a space appears in their name. Should Fix Later.

# TO-DO LIST:
- [Ref. #18] Clean README.md again for the v1.0 release
- [Ref. #17] Convert tracking of plex tv-shows from "in-progress" to "watched" flag, possibly a combination of both
- [Ref. 16] Add logger and beautify output, preferably with summeries
- [Ref. 15] Beautify Output texts
- [Ref. 9] Convert to an executable or package within pip; additionally, the docker container should be started back up!
- [Ref. 6] Have option to download specials after show is over
- [Ref. ###] When all of a "ended" show is finsihed being watched downgrade via profile change - MAYBE
- [Ref. ###] A configuration file cold be added which would allow specific user selection on a multi-user server that would allow for only specific users to be watched - MAYBE

# TESTED ON:
- PRODUCTION VERSIONS v0.2.0 and Above
    - Both of the below versions were tested on a LAN enviroment with access available from the outside WAN. 11 total user accounts, 10 of which have consumed some content, but some are MOVIE ONLY watchers and have no interest in television, the script can handle all these exceptions that occur when an account has no in-progress TV Shows.
