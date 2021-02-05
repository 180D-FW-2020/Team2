@echo off
conda create --name WAP --force -y ^
&& echo "created env" ^
&& conda activate WAP ^

&& echo "Installing python==3.7.6" ^
&& conda install -y python==3.7.6 ^

&& echo "Installing git" ^
&& conda install -y -c anaconda git ^

&& echo "Installing tensorflow" ^
&& conda install -y tensorflow ^

&& echo "cloning repo" ^
&& call git clone https://github.com/180D-FW-2020/Team2.git ^

&& echo "installing dill" ^
&& conda install -y --satisfied-skip-solve -c conda-forge dill ^

&& echo "installing fire" ^
&& conda install -y --satisfied-skip-solve -c conda-forge fire ^

&& echo "installing matplotlib " ^
&& conda install -y --satisfied-skip-solve -c conda-forge matplotlib ^

&& echo "installing psutil " ^
&& conda install -y --satisfied-skip-solve -c conda-forge psutil ^

&& echo "installing pycocotools " ^
&& call pip install pycocotools ^

&& echo "installing requests " ^
&& conda install -y --satisfied-skip-solve -c conda-forge requests ^

&& echo "installing scikit-image" ^
&& conda install -y --satisfied-skip-solve -c conda-forge scikit-image ^

&& echo "installing scipy" ^
&& conda install -y --satisfied-skip-solve -c conda-forge scipy ^

&& echo "installing slidingwindow" ^
&& conda install -y --satisfied-skip-solve -c conda-forge slidingwindow ^

&& echo "installing tqdm" ^
&& conda install -y --satisfied-skip-solve -c conda-forge tqdm ^

&& echo "Installing tensorpack" ^
&& call pip install git+https://github.com/ppwwyyxx/tensorpack.git ^

&& echo "installing swig" ^
&& conda install -y swig ^
&& echo "cding" ^
&& call cd Team2/tf-pose-estimation-master/tf_pose/pafprocess ^
&& echo "swig" ^
&& swig -python -c++ pafprocess.i && python setup.py build_ext --inplace && echo "Installing opencv" ^
&& call pip install opencv-python ^
&& call pip install git+https://github.com/adrianc-a/tf-slim.git@remove_contrib ^
&& call cd ../../models/graph/cmu ^
&& download.sh ^
&& call cd ../../../.. ^

&& echo "Installing kivy" ^
&& conda install -y -c conda-forge kivy ^
&& echo "Installing paho-mqtt" ^
&& conda install -y -c conda-forge paho-mqtt ^
&& echo "Installing pyaudio" ^
&& conda install -y -c anaconda pyaudio ^
&& echo "Installing speech recognition" ^
&& conda install -y -c conda-forge speechrecognition ^
&& echo "Installing google cloud speech" ^
&& call pip install google-cloud-speech ^
&& echo "Installing playsound" ^
&& call pip install playsound ^
&& conda deactivate
