from future.utils import with_metaclass
from stopeight.util.runnable import *

class ScribblePoint(tuple):
    def __init__(self,lis):
        self.first = lis[0]
        self.second = lis[1]

class ScribbleData(list):
    def __init__(self):
        super(list,self).__init__()

    def append(self,something):
        if type(something)!=ScribblePoint:
            raise Exception("Please only use ScribblePoint in ScribbleData.")
        super(ScribbleData,self).append(something)
        
#class ScribbleData(list):#(with_metaclass(Singleton,list)):
#class ScribbleData(Singleton):
    #def __init__(self, **kwargs):
    #    super(ScribbleData,self).__init__(**kwargs)

class ScribbleBackup(ScribbleData):
#class ScribbleBackup(list):#(with_metaclass(Singleton,list)):
#class ScribbleBackup(Singleton):
    pass

#from stopeight.util.editor.scribble import ScribbleArea
#class ScribbleDisplay(with_metaclass(Singleton,ScribbleArea)):
#    pass

from numpy import ndarray
class WaveData(ndarray):
    pass
#class WaveData(with_metaclass(Singleton,ndarray)):
#class WaveData(Singleton):
