#!/bin/bash

command_arr=(dill fire matplotlib psutil pycocotools requests scikit-image scipy slidingwindow tqdm )
conda create --name WAP --force -y
eval "$(conda shell.bash hook)"
conda activate WAP

echo "Installing python==3.7.6"
conda install -y python==3.7.6

echo "Installing git"
conda install -c -y anaconda git

echo "Installing tensorflow"
conda install -y tensorflow

git clone https://github.com/180D-FW-2020/Team2.git
cd Team2/tf-pose-estimation-master

for i in "${command_arr[@]}"
do
	echo "COMMAND: " $i
	conda install -y --satisfied-skip-solve -c conda-forge $i
done
pip install git+https://github.com/ppwwyyxx/tensorpack.git

conda install -y swig
cd tf_pose/pafprocess
swig -python -c++ pafprocess.i && python setup.py build_ext --inplace

echo "Installing opencv"
pip install opencv-python
pip install git+https://github.com/adrianc-a/tf-slim.git@remove_contrib
cd ../../models/graph/cmu
download.sh
cd ../../../..

echo "Installing kiv"
conda install -y -c conda-forge kivy
conda install -y -c conda-forge paho-mqtt
conda install -y -c anaconda pyaudio
conda install -y -c conda-forge speechrecognition
pip install google-cloud-speech
pip install playsound
conda deactivate
