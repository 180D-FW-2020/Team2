# wellness and productivity (WAP)
Michelle Lam, Michelle Tan, Jackie Lam, & Isabel Ketner

## overview
WAP is a device that aims to improve one's physical and mental health via personalized wellness exercises the user can be reminded to complete throughout the day.

## how to run
change the name in ID.txt to be `firstnamelastname` \
on your laptop, enter the command `python main.py` \
on your rpi, enter the command `python rpi-main.py`

## structure
**main.py**  runs application on laptop \
**helper.py** helper functions + constants for main.py \
**rpi-main.py** driving function on raspi \
**imu** rpi \
+-- python-BerryIMU-gryo-accel-compass-filters \
+-- +-- berryIMU_classifier.py \
**mqtt** rpi + laptop \
+-- pub.py \
+--sub.py \
**matrix** rpi \
+--matrix_functions.py \
**speech** laptop \
+-- audio_msg.py \
**ui** laptop \
+-- screen.kv

## setup
within your conda environment, run \
`conda install -c conda-forge wheel` \
`conda install -c anaconda pip` \
`python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew` \
`python -m pip install kivy.deps.gstreamer` \
`python –m pip install kivy`\
`conda install -c conda-forge paho-mqtt`
