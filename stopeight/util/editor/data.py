from future.utils import with_metaclass
from stopeight.util.runnable import *

class ScribblePoint(tuple):
    def __init__(self,lis):
        """ Same signature as stopeight-clibs timecode"""
        self.x = lis[0]
        self.y = lis[1]

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,x):
        self.x=x
    def set_y(self,y):
        self.y=y

from numpy import ndarray
import numpy as np
class ScribbleData(ndarray):
    def __new__(cls,*args,**kwargs):
        try:
            if kwargs['size']>1:
                kwargs['shape']=(kwargs['size'])
            else:
                kwargs['shape']=(1)
            del kwargs['size'] 
        except KeyError:
            kwargs['shape']=(1)
        kwargs['dtype']= np.dtype({'names':['coords','type'], 'formats':[('<f8', (2,)),'<i4'], 'offsets':[0,16], 'itemsize':24})
        return super(ScribbleData,cls).__new__(cls,*args,**kwargs)
#    def __init__(self):
#        super(list,self).__init__()
#
#    def append(self,something):
#        if type(something)!=ScribblePoint:
#            raise Exception("Please only use ScribblePoint in ScribbleData.")
#        super(ScribbleData,self).append(something)
        
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

class WaveData(ndarray):
    pass
#class WaveData(with_metaclass(Singleton,ndarray)):
#class WaveData(Singleton):
