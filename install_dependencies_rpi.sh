#!/bin/bash

conda create --name W_RPI --force -y
eval "$(conda shell.bash hook)"
conda activate W_RPI

echo "Installing python==3.7.6"
conda install -y python==3.6.1

echo "Installing git"
conda install -y -c anaconda git

git clone https://github.com/180D-FW-2020/Team2.git

sudo usermod -a -G spi,gpio pi

echo "installing python libraries"
sudo apt install build-essential python3-dev python3-pip libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5

echo "installing setup tools"
sudo -H pip install --upgrade --ignore-installed pip setuptools

echo "install matrix packages"
sudo -H pip install --upgrade luma.led_matrix

echo "install paho for mqtt"
sudo pip install paho-mqtt

echo "finished rpi installation!"
