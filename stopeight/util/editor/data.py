from future.utils import with_metaclass
from stopeight.util.runnable import *

class ScribbleData(list):#(with_metaclass(Singleton,list)):
#class ScribbleData(Singleton):
    #def __init__(self, **kwargs):
    #    super(ScribbleData,self).__init__(**kwargs)
    pass

class ScribbleBackup(list):#(with_metaclass(Singleton,list)):
#class ScribbleBackup(Singleton):
    pass

#from stopeight.util.editor.scribble import ScribbleArea
#class ScribbleDisplay(with_metaclass(Singleton,ScribbleArea)):
#    pass

from numpy import ndarray
class WaveData(ndarray):#(with_metaclass(Singleton,ndarray)):
#class WaveData(Singleton):
    pass
