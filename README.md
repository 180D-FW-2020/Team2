# wellness and productivity (WAP)
Michelle Lam, Michelle Tan, Jackie Lam, & Isabel Ketner

## set up
For information on how to use our product, you can find our user manual [here](https://docs.google.com/document/d/1SdeEpSudTallBMvt7lm1ykPYXnIb84JsA82q6huSv1o/edit?usp=sharing).

### config.txt
config.txt allows the user to switch between different modes they want to run (mostly for debugging purposes).

options for mode are [(debug,seconds), (debug,minutes) regular, (limited,#)]
debug - choose between 30s, 60s, 90s intervals, or 3min, 6min, 9min intervals
regular - as expected on selection screen
limited - only runs activities for certain amount of time intervals (in seconds) specified by #, then sits in wait screen forever

## source code
All files are completed unless otherwise noted.

| File Name | Description |
|---| --- |
| App_Executable | Code to package the product using PyInstaller. WIP. <br/> **More details inside folder.**|
| IMU | Contains code relevant to gesture recognition, including libraries, configuration, and scripts.<br/> **More details inside folder.** |
| MQTT | Pub and sub classes for cross device communication. <br/> **More details inside folder.**|
| Matrix | Libraries and scripts to use the LED Matrix, when connected to a raspberry pi.<br/> **More details inside folder.** |
| Mood_Tracker | Class to generate a playlist from Spotify API. <br/> **More details inside folder.**|
| Speech | Class to process and transcribe audio input.<br/> **More details inside folder.** |
| Stats | Class to update user statistics in Google Firebase.<br/> **More details inside folder.** |
| UI | Contains all images and styling. <br/> **More details inside folder.**| 
| tf-pose-estimation-master | Contains all relevant libraries and scripts for pose recognition.<br/> **More details inside folder.** |
| config.txt | Stores user data and mode preference. |
| helper.py | Additional functions called by main.py for use in activities. |
| install_dependencies.* | Create and install a conda environment on the user's laptop. <br/>.sh for Unix-based systems, .bat for Windows systems |
| install_rpi.sh | Create and install a conda environment on the user's raspberry pi. |
| main.py | Main application code. Runs on the user's laptop |
| rpi-main.py | Main application code. Runs on the user's raspberry pi. |
| rpi_conn.py | Handles connection and communication with the raspberry pi. |
| test_msg_sub.py | Receives all MQTT messages, changes state of main application based on these messages. |
