# wellness and productivity (WAP)
Michelle Lam, Michelle Tan, Jackie Lam, & Isabel Ketner

## overview
WAP is a device that aims to improve one's physical and mental health via personalized wellness exercises the user can be reminded to complete throughout the day.

## how to run
change the name in ID.txt to be `firstnamelastname` \
on your laptop, enter the command `python main.py` \
on your rpi, enter the command `python rpi-main.py`

## laptop setup
`conda create --name WAP` \
`conda activate WAP` \
`conda install python==3.7.6` \
`conda install -c anaconda git` \
`conda install tensorflow` \
`git clone https://github.com/180D-FW-2020/Team2.git` \
`cd tf-pose-estimation-master` \
`pip install -r requirements.txt` \
`conda install swig` \
`cd tf_pose/pafprocess` \
`swig -python -c++ pafprocess.i && python setup.py build_ext --inplace` \
`pip install opencv-python` \
`pip install git+https://github.com/adrianc-a/tf-slim.git@remove_contrib` \
`cd ../../models/graph/cmu` \
`download.sh` \
`cd ../../../..` \
`conda install -c conda-forge kivy` \
`conda install -c conda-forge paho-mqtt`\
`conda install -c anaconda pyaudio` \
`conda install -c conda-forge speechrecognition` \
`pip install google-cloud-speech` \
`pip install playsound`

### tips n tricks
if tensorflow issues persist, run the command `pip install tensorflow-estimator==2.1.*` in your conda environment

## raspberry pi setup
[todo]
