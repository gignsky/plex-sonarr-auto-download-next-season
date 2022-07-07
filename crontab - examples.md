# THERE IS NO REASON TO CRONTAB THE SCRIPT IN MANUAL MODE AS IT REQUIRE USER INPUT IN THE BEGINNING STAGES

# run python script on every 10 minutes of the hour

*/10 * * * * {PATH_TO_PYTHON3} /APPLICATION_DIRECTORY/main.py auto > {SCRIPT_OUTPUT_DIR}/script_output.txt

# PATH_TO_PYTHON3
	- Can be found with "which python3" on linux servers
	- Default /usr/bin/python3

# SCRIPT_OUTPUT_DIR
	- navigate to directory you would like debug script to run if you want a debug output after each automatic run
	- on linux system type "touch script_output.txt"
	- in that directory type "pwd" to get value for {SCRIPT_OUTPUT_DIR}