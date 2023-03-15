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
## Bug Fixed:
fixed issue with sonarr struggling to aquire appropriate season number indexes issue #7 on github

# V0.5.0
# The Great Reunification
script structure was cleaned up and made more uniform and made easier to edit
additionally the script was unified into one single file that can be run;
    - to run manually run "python3 main.py"
    - to run in automatic mode run "python3 main.py auto"
    - for help run "python3 main.py help"

# V0.5.1
## Bug Fix
fixed issue #35

# V0.5.2
## Bug Fix
fixed issue #40

# V0.5.3
## Bug Fix
fixed issue #43
fixed issue #44

# V0.5.4
## Bug Fix
fixed issue with monitor season not being given next season key unreported in issues but will be updated in releases

# V0.5.5
## Bug Fix
fixed issues where a plex show with no guid errored out the whole script ref. issue #53
added time output to beginning of output for help with troubleshooting ref. issue #52

# V0.5.6
## Bug Fix
dependabot update: bump setuptools from 59.6.0 to 65.5.1

# V0.5.6c
## Dependency Update
dependabot update: Bump astroid from 2.13.3 to 2.14.2 #98
dependabot update: Bump pylint from 2.15.10 to 2.16.2
dependabot update: Bump stevedore from 4.1.1 to 5.0.0
dependabot update: Bump pathspec from 0.10.3 to 0.11.0
dependabot update: Bump setuptools from 65.5.1 to 67.4.0

# V0.5.6d
## Dependency Update
dependabot update: Bump pylint from 2.16.2 to 2.17.0 #108
dependabot update: Bump platformdirs from 2.6.2 to 3.1.1 #107
dependabot update: Bump charset-normalizer from 3.0.1 to 3.1.0 #105
dependabot update: Bump typing-extensions from 4.4.0 to 4.5.0 #104
dependabot update: Bump black from 22.12.0 to 23.1.0 #103
