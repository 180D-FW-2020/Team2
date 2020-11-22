IMU CALIBRATION (Optional):

- Run the calibration script under IMU/python-BerryIMU-gyro-accel-compass-filters:
	python3 calibrateBerryIMU.py
	
- Rotate the IMU in all directions. After about 30 seconds when the values 
  are not changing, press Ctrl-C. 

- This will save the data in a file named "calibration.csv" (do not delete)


IMU CONTROLLER:

- Run the classifier script:
	python3 berryIMU_classifier.py

- Using the controller:
    Right Rotation: Activate reminders
    Left Rotation: Alert network after finishing task
    Vertical Shake: Begin audio recording for voice messages
    Horizontal Shake: Snooze reminders
