# Copyright (C) 2018 Fassio Blatter

from stopeight.util import runnable
from sys import modules as loader

from PyQt5.QtWidgets import QComboBox,QPushButton

from stopeight.logging import logSwitch
log = logSwitch.logPrint()
_LOGDIR = '.stopeight' # this is not for logging messages; it is for data files

class Algorithm_Select(QComboBox):
    def __init__(self, module, **kwargs):
        super(Algorithm_Select,self).__init__(**kwargs)
        self.module = module
        
        module_name = module[0]
        import types
        for key in dir(loader[module_name]):
            if not key.startswith('_'):
                if isinstance(loader[module_name].__dict__[key],types.BuiltinFunctionType) or \
                isinstance(loader[module_name].__dict__[key],types.FunctionType):
                    self.addItem(loader[module_name].__dict__[key].__name__)

from stopeight.util.editor_data import ScribbleData, ScribbleBackup
class Algorithm_Run(QPushButton):
    def __init__(self, module, **kwargs):
        super(Algorithm_Run,self).__init__(**kwargs)
        self.setText("Run")
        self.module = module

    @staticmethod
    def _auto_out(module_name,package_type,function_name):
        top = module_name+'.'+function_name
        import os
        from subprocess import check_output
        sub = 'HEAD'
        if (package_type==True):
            #get head from current directory (os.getcwd()).endswith('stopeight')
            try:
                sub = check_output(['git','rev-parse','--short','HEAD']).decode('utf-8').rstrip()
            except:
                sub = check_output(['git','rev-parse','--short','HEAD']).rstrip()
        else:
            #get head from stopeight-clibs
            try:
                sub = check_output(['git','rev-parse','--short','HEAD'],cwd=os.path.join('stopeight-clibs')).decode('utf-8').rstrip()
            except:
                sub = check_output(['git','rev-parse','--short','HEAD'],cwd=os.path.join('stopeight-clibs')).rstrip()
        top = os.path.join(top,sub)
        return top
    
    def _identify(self,scribblearea):
        import os
            
        #if (os.getcwd()).endswith('stopeight'):
        #    if (self.select.module_name=='stopeight.util.file'):
        if hasattr(scribblearea,'tablet_id'):
            sub = str(scribblearea.tablet_id)
        else:
            sub = 'MouseData'
        return sub
        
    def run(self,currentText):
        #inspect.signature()[return]
        #if (len(self.select.module[2].OUTPUT)>0):
        #    self.select.module[2].INPUT = self.select.module[2].OUTPUT
        #    self.select.module[2].OUTPUT= []
        #currentText = self.select.currentText()
        import time
        time = time.time()
        data = ScribbleData()
        backup = ScribbleBackup()#get singleton
        backup[:] = data#assign copy
        try:
            log.info("Invoking "+currentText+" with "+str(len(data))+" data sets...")
            data[:] = loader[self.module[0]].__dict__[currentText](data)
            #if backup == data:
            #    raise Exception("Backup not successful or function values unchanged")
            log.info("Size after call: Input "+str(len(backup))+", Output "+str(len(data)))
        #except:
        except BaseException as e:
            log.error("Error during method invokation: "+self.module[0]+'.'+currentText)
            
            from stopeight.util import file
            from os.path import expanduser,join
            file._write(backup,time,outdir=join(expanduser("~"),_LOGDIR
                                                ,self._auto_out(self.module[0],self.module[1],currentText)
                                                #,self._identify(_DATA['MyScribble'])
                                                ))
            del data[:]
            if (len(data)>0):
                raise Exception("Data clear failed!")
            log.error(e)
        
class Connector:
    def __init__(self,command,outputObject):
        self._output = outputObject
        self.select = Algorithm_Select(command)
        self.button = Algorithm_Run(command)
        self.button.clicked.connect(self.run)

    def run(self):
        log.debug(self.select.currentText())
        self.button.run(self.select.currentText())
        log.debug(str(len(ScribbleData())))

from PyQt5.QtCore import Qt        
class ScribbleConnector(Connector):
    def __init__(self,command,scribble):
        super().__init__(command,scribble)
        self.colors = [Qt.blue, Qt.red]

    def run(self):
        super().run()
        self._output.clearImage()
        #for d,c in self.data,self.colors:
            #self.scribble.plot(d,c)
        self._output.plot(ScribbleBackup(),self.colors[1])
        self._output.plot(ScribbleData(),self.colors[0])

#class WaveConnector(Connector):
#    def __init__(self,command,scribble):
#        super().__init__(command,[WaveData()],scribble)

#    def run(self):
#        super().run()
