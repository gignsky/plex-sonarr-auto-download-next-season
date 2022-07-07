# Ensure python3 is installed

sudo apt install python3 -y

# If you don't have pip

sudo apt install python3-pip -y

# Neccecary

python3 -m pip install requests plexapi -y


# Only install arrapi if you decided to turn on season monitoring setting in monitor_master.py

python3 -m pip install arrapi -y
