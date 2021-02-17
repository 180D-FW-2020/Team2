# IMU Setup

Install the necessary components
```
$ sudo apt-get update
$ sudo apt-get upgrade
$ conda upgrade conda
$ conda update conda
$ pip install --upgrade pip
$ sudo apt-get install git i2c-tools libi2c-dev
$ conda install -c conda-forge smbus2
```

Try opening the blacklist file:
```
$ sudo nano /etc/modprobe.d/raspi-blacklist.conf
```
If the file is empty or it does not exist, you can keep going. Otherwise, if there is the line
blacklist i2c-bcm2708, put a ‘#’ in front to comment this line out.

Add the two lines into `/etc/modules` using a text editor
```
i2c-dev
i2c-bcm2708
```

Add the two lines into `boot/config.txt`
```
dtparam=i2c_arm=on
dtparam=i2c1=on
```

Reboot your Raspberry Pi
```
$ sudo reboot -h now
```

IMU installation is complete!

# IMU Calibration (Optional):
Run the calibration script under `IMU/python-BerryIMU-gyro-accel-compass-filters`
```
$ python3 calibrateBerryIMU.py
```
	
Rotate the IMU in all directions. After about 30 seconds when the values are not changing, press Ctrl-C. 

This will save the data in a file named `calibration.csv` (do not delete)


# IMU Controller:
Run the classifier script:
```
python3 berryIMU_classifier.py
```

Using the controller:
```
Vertical Shake: Activate reminders
Horizontal Shake: Send a congrats message (to be implemented)
```



