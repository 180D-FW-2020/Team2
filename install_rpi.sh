#!/bin/bash

echo "Creating conda environment"
conda create --name WAP --force -y
echo "set report errors"
conda config --set report_errors false
echo "activate conda environment"
conda activate WAP

echo "install IMU packages"
sudo apt-get install -y git i2c-tools libi2c-dev
conda install -y -c conda-forge smbus2
sudo usermod -a -G spi,gpio pi

echo "Installing python==3.6.1"
conda install -y python==3.6.1

echo "installing python libraries"
sudo apt install build-essential python3-dev python3-pip libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5

echo "installing setup tools"
sudo -H pip install --upgrade --ignore-installed pip setuptools

echo "install matrix packages"
pip install luma.led_matrix

echo "install paho for mqtt"
pip install paho-mqtt

echo "finished rpi installation!"
