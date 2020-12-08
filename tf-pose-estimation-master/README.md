
### Intro
Hey! This is a clone of the tf-pose-estimation by Ildoo Kim modified to work with Tensorflow 2.0+!
Link to original repo: https://www.github.com/ildoonet/tf-openpose

# Getting Started
### Web Tutorial on installing the necessary dependencies: https://medium.com/@gsethi2409/pose-estimation-with-tensorflow-2-0-a51162c095ba

### Video Tutorial Alternative: https://youtu.be/NjygefpyCcc

Here is a list of the steps one needs to take for ease of accessibility:
### 1. Install anaconda/miniconda.
I used anaconda, because my anaconda don't want none unless you got buns hun.
**Download here:** https://www.anaconda.com/products/individual

### 2. Create a new virtual conda environment.
A conda environment is a directory that contains a specific collection of conda packages that you have installed. For example, you may have one environment with NumPy 1.7 and its dependencies, and another environment with NumPy 1.6 for legacy testing.
```
conda create —-name AIMachine
```

### 3. Activate your virtual environment. If you don't you will probably get import module errors.
```
conda activate AIMachine
```

### 4. Install Python. You can probably update the python 3 version, but you will probably run into issues if you have python 2.
```
conda install python==3.7.6
```

### 5. Install the latest version of Tensorflow. I used version 2.3.1. You can check the version of the module by typing: pip show tensorflow.
```
conda install tensorflow
```

Optional reading: https://docs.anaconda.com/anaconda/user-guide/tasks/tensorflow/

### 6. Create a new working directory in your terminal and go into the folder.
```
mkdir myWorkspace
cd myWorkspace
```

### 7. Clone the repo created by Gunjan Sethi
```
git clone https://github.com/gsethi2409/tf-pose-estimation.git
```

### 8. Enter the folder and install the requirements.
```
cd tf-pose-estimation
pip install -r requirements.txt
```

If this doesn't work, look at the requirements within requirements.txt, and try to individually "conda install <module" the modules. "conda install ..." sometimes doesn't work too, so try "conda install -c conda-forge <module>" or even with "pip install".
```
argparse
dill
fire
matplotlib
numba
psutil
pycocotools
requests
scikit-image
scipy
slidingwindow
tqdm
git+https://github.com/ppwwyyxx/tensorpack.git
```
### 9. Install SWIG. Windows users might need to download a certain version of swig for Windows. More details here: http://www.swig.org/download.html.
```
conda install swig
```

### 10. Build C++ library for post-processing.
```
cd tf_pose/pafprocess
swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
```
### 11. Install OpenCV.
```
pip install opencv-python
```
Alternatively, you can do:
```
conda install -c conda-forge opencv
```

### 12. Install tf-slim library.
```
pip install git+https://github.com/adrianc-a/tf-slim.git@remove_contrib
```

### 13. Download Tensorflow Graph File(pb file).
```
cd models/graph/cmu
sudo bash download.sh
cd ../../..
```

### 14. Run a quick test with an image!
```
python run.py --model=mobilenet_thin --resize=432x368 --image=./images/p1.jpg
```

### 15. Run a quick test with a webcam!
```
python run_webcam.py --model=mobilenet_thin --resize=432x368 --camera=0
```

# To run our pose determination script, "run_compare_ref_test_webcam.py":

You need to specify the reference pose as <pose_name>:
```
python run_compare_ref_test_webcam.py --pose=<pose_name(s)>
```

Example:
```
python run_compare_ref_test_webcam.py --pose=squat,tree
```

# To add your own reference pose, you will need to do the following:
Run script by specifying the pose you want to create a reference for (e.g. squat). This is a requirement**
1. python timed_capture.py --ref_pose=<pose_name> (e.g. python timed_capture.py --ref_pose=squat)
2. To start the timer, press tje spacebar (you might have to click on the window with the webcam first so it can register the key press)
3. The timer is by default 7 seconds, but you can change it by passing in --timer=<num_seconds> (e.g. python timed_capture.py --ref_pose=squat --timer=10)
4. Once the timer is done, the reference image will be saved in images/references/<pose_name>_reference.jpg, which can be used to find the joints
```
python timed_capture.py --ref_pose=<pose_name> --timer=10
```

## **The only files/folders you will need to know about are just:**
- run_compare_ref_test_webcam.py
- timed_capture.py
- images/references
