# ui testing

## pyqt5

### setup
within your conda environment, run `conda install -c anaconda pyqt`
used [this tutorial](https://www.geeksforgeeks.org/pyqt5-qcheckbox/) for reference

### pros + cons
pros
- easy to get up and running
- extensive documentation
- very low latency
- can set style preferences directly within the app, instead of having to make external files
- platform independent
cons
- looks old and ugly -- would take some effort to make it visually pleasing
- limited animations, would have to write our own libraries for it
- "freezing" the app is harder than usual, would have to use fbs instead of pyinstaller

## kivy

### setup
within your conda environment, run
`conda install -c conda-forge wheel`
`conda install -c anaconda pip`
`python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew`
`python -m pip install kivy.deps.gstreamer`
`python –m pip install kivy`

### pros + cons
pros
- extensive documentation
- platform independent
- lot of opportunity to build out and make more complex
- easy to change the design, looks new and fresh
- easy to add in animations
- can package using pyinstaller
cons
- slower
- need to have additional .kv files
- larger learning curve because additional complexity

## which one to choose

pyqt if we want the UI to remain simple and fit our immediate needs, kivy if we want
to be able to make the UI more complex/pretty + add in animations
