# Description
Subfolder contains reference images for the application background and additional images shown on the screen, as well as the kv file (the kivy equivalent of a .css file). 
All styling goes here. All designs are custom made by Michelle Lam.

# Installation
The following packages were used to create the UI and are installed when running the installation script "install_dependencies.sh" or "install_dependencies.bat".

The primary package used for the product's UI is kivy, which can be installed below:
```
$ conda install -y -c conda-forge kivy
```

Daily task stats were displayed using the following packages:
```
$ pip install kivy-garden
$ garden install graph
$ pip install matplotlib==3.1.3
$ garden install matplotlib
```
