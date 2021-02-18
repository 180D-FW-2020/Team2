import os

path = os.getcwd()
files = ["../ID.txt", "../UI/screen.kv", "../UI/holo-01.png"]
#create_exec_command = "pyinstaller main.py --onefile --add-data ID.txt:" + path
create_exec_command = "pyinstaller main.py --add-data .:."
os.system(create_exec_command)

# copy_main_command = "cp ./dist/main ./main"
# os.system(copy_main_command)

pyinstaller main.py --add-data .:.

pyinstaller main.py --onefile --hidden-import=run_compare_ref_test_webcam --hidden-import tf_pose --add-data ID.txt:. --add-data ./UI/*:UI --add-data ./tf_pose_estimation_master/run_compare_ref_test_webcam.py:tf_pose_estimation_master --add-data ./tf_pose_estimation_master/images/references/*:tf_pose_estimation_master --add-data ./tf_pose_estimation_master/sounds/*:tf_pose_estimation_master --add-data ./Speech/SentAudio/*:Speech/SentAudio --add-data ./Speech/SentTxt/*:Speech/SentTxt

pyinstaller run_compare_ref_test_webcam.py --onefile --add-data ./images/references/*:images/references --add-data ./sounds/*:sounds

pyinstaller run_compare_ref_test_webcam.py --onefile --hidden-import=tensorflow_core

pyinstaller --noupx --hidden-import=tensorflow_core --hidden-import=tensorflow_core.lite.python.lite -F run_compare_ref_test_webcam.py

pyinstaller -F --noupx --log-level=WARN --additional-hooks-dir=hooks run_compare_ref_test_webcam.py

bundle_dir = Path(getattr(sys, '_MEIPASS', Path.cwd()))
try:
    print("Executable directory: ", bundle_dir)
    os.chdir(bundle_dir)
    print(os.listdir("."))
except:
    print("Something wrong with specified directory. Exception- ", sys.exc_info()) 