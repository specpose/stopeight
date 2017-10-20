import os,sys
exec_dir = os.path.abspath(os.path.join(os.getcwd(),os.pardir))
file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
if (exec_dir==file_dir):
    raise Exception("This script should not be run from inside the module's directories.")

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]

from future.utils import with_metaclass
from stopeight.util.runnable import Singleton
class SingletonList(with_metaclass(Singleton,list)):
    pass

##class Singleton(list):
##    _instance = None
##    def __new__(cls, *args, **kwargs):
##        if not cls._instance:
##            cls._instance = list.__new__(cls, *args, **kwargs)
##            print("new instance created")
##        return cls._instance
##    def __init__(self):
##        print("init method called")

if __name__ == '__main__':
    test1 = SingletonList()
    test1.append("5")
    if (len(test1)!=1):
        raise "test1 assignment failed!"
    test2 = SingletonList()
    test2.append("7")
    if (len(test2)!=2):
        raise "test2 assignment failed!"
    if (len(test1)!=len(test2)):
        raise "Singleton instantiation test failed!"
    else:
        print(test1)
        print(test2)
