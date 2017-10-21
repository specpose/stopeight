from future.utils import with_metaclass
from stopeight.util.runnable import *

class ScribbleData(with_metaclass(Singleton,list)):
#class ScribbleData(Singleton):
    #def __init__(self, **kwargs):
    #    super(ScribbleData,self).__init__(**kwargs)
    pass

class ScribbleBackup(with_metaclass(Singleton,list)):
#class ScribbleBackup(Singleton):
    pass

#import numpy
#class WaveData(Singleton):
#    pass
