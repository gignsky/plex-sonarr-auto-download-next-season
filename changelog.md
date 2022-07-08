# ORIGINAL VERSION v0.1.0
The original script was tested on a local environment with two active plex users, so your mileage may vary on larger installs.

# PRODUCTION VERSIONS v0.2.0 and Above
Both of the below versions were tested on a LAN enviroment with access available from the outside WAN. 11 total user accounts, 10 of which have consumed some content, but some are MOVIE ONLY watchers and have no interest in television, the script can handle all these exceptions that occur when an account has no in-progress TV Shows.

# V0.3.1
# Feature added:
The intention here is to download the remaining episodes in the first season if the pilot episode that was downloaded has been completed

# V0.4.0
# Feature added:
added pilot episode feature

# V0.4.1
# Bug Fixed:
fixed issue with sonarr struggling to aquire appropriate season number indexes issue #7 on github

# V0.5.0
# The Great Reunification
script structure was cleaned up and made more uniform and made easier to edit
additionally the script was unified into one single file that can be run;
    - to run manually run "python3 main.py"
    - to run in automatic mode run "python3 main.py auto"
    - for help run "python3 main.py help"

# V0.5.1
# BUG FIX
fixed issue #35

# V0.5.2
# BUG FIX
fixed issue #40

# V0.5.3
# BUG FIX
fixed issue #43
fixed issue #44
