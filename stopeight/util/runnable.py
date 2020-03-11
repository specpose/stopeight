# Copyright (C) 2017 Fassio Blatter

import os,sys
exec_dir = os.path.abspath(os.path.join(os.getcwd(),os.pardir))
file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
if (exec_dir==file_dir):
    raise Exception("This script should not be run from inside the module's directories.")

try:
    # new location for sip
    # https://www.riverbankcomputing.com/static/Docs/PyQt5/incompatibilities.html#pyqt-v5-11
    from PyQt5 import sip
except ImportError:
    from PyQt5 import QtCore
    import sip

from PyQt5.QtWidgets import QApplication,QMainWindow
class EditorApp(QApplication):
    _instance = None
    window = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(EditorApp,cls).__new__(cls)
        return cls._instance
    def __init__(self):
        if not self.window:
            import sys
            super(EditorApp,self).__init__(sys.argv)
            self.window = QMainWindow()
            self.window.setWindowTitle("Editor")

#inherit: (StatefulClass,metaclass=Singleton)
class Singleton(type):
    _instances = {}
    ## type.__call__ is type(), not type()() unlike object()()
    def __call__(cls, *args, **kwargs):
    #    print(str(cls)+"__call__")
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    ## Prohibited!
    # def __new__(cls, *args, **kwargs):
    #     print(str(cls)+"__new__")
    #     super(Singleton,cls).__new__(cls,*args, **kwargs)
    def __init__(cls, *args, **kwargs):
    #    print(str(cls)+"__init__")
        super(Singleton,cls).__init__(*args, **kwargs)

class SingletonList(list,metaclass=Singleton):
    pass
import numpy
from numpy import ndarray
class SingletonNumpy(ndarray,metaclass=Singleton):
    def __call__(cls, *args, **kwargs):
        print("__call__ sub")

##class Singleton(object):
##    _instance = None
##    def __new__(cls,name,bases,dict):
##        if not cls._instance:
##            cls._instance = object.__new__(cls)
##        return cls._instance
##    def __init__(cls,name,bases,dict):
##        pass

##class SingletonList(Singleton(list)):
##    pass
##import numpy
##class SingletonNumpy(Singleton(numpy)):
##    pass

if __name__ == '__main__':
    print("__main__")
    test1 = SingletonList()
    test1.append("5")
    print(test1)
    if (len(test1)!=1):
        raise Exception("test1 assignment failed!")
    test2 = SingletonList()
    test2.append("7")
    print(test2)
    if (len(test2)!=2):
        raise Exception("test2 assignment failed!")
    if (len(test1)!=len(test2)):
        raise Exception("Singleton instantiation test failed!")
    test3 = SingletonNumpy(shape=(1,),dtype=numpy.int16)
    test3 = SingletonNumpy()
    print(test3[0])
