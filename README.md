# raspberrypi
If this code is to work then you have to run the following commands on the raspberry pi:

# Upgrade the Pi:
sudo apt update 
<br />
sudo apt full-upgrade
<br />
This will update any packages and dependecies on the pi, and will give it a full upgrade to the latest firmware.

# Install the sense-hat module:
sudo apt-get install sense-hat
<br />
This will install the sense-hat module, so we can integrate it with python.

# Directories
In order for the mp3 files to play, make sure they are in the same directory as the python file.

# What is a Sense HAT?
The Sense HAT is an add-on board for the Raspberry Pi, made especially for the Astro Pi competition. 
The board allows you to make measurements of temperature, humidity, pressure, and orientation, and to output information using its built-in LED matrix.
If you have any issues with setting it up, I suggest you follow this guide, https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat
