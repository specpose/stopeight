# stopeight

Python2 branch of stopeight. stopeight versions 3 and above do not work with Python version 2 of the Python interpreter anymore.

This build has been tested on Ubuntu 18.04.

1. PyQt5 has been removed from PyPI/pip2. It is required for the editor. It is available from the Universe repository.
+
$ sudo apt-get install python-pyqt5

2. Install the following minimal requirements from the main repository.
+
$ sudo apt-get install python python-pip

3. Clone the Python2 branch of the Github repository recursively.
+
$ git clone --recurse-submodules https://github.com/specpose/stopeight.git
$ git checkout Python2

4. If you want to run the tests for the legacy algorithm, install Qt5.
+
$ sudo apt-get install qtbase5-dev

5. Build in the stopeight directory.
+
$ cd stopeight
$ python setup.py install --user
