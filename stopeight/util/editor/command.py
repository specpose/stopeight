# Copyright (C) 2018 Fassio Blatter

from stopeight.util import runnable
from sys import modules as loader

from PyQt5.QtWidgets import QComboBox,QPushButton

from stopeight.logging import logSwitch
log = logSwitch.logPrint()
_LOGDIR = '.stopeight' # this is not for logging messages; it is for data files

from funcsigs import signature
class Algorithm_Select(dict):
    def __init__(self, module, **kwargs):
        super(Algorithm_Select,self).__init__(**kwargs)
        self._module = module
        
        module_name = self._module[0]
        import importlib
        importlib.import_module(module_name)
        import types
        for key in dir(loader[module_name]):
            if not key.startswith('_'):
                builtin = isinstance(loader[module_name].__dict__[key],types.BuiltinFunctionType)
                dynamic = isinstance(loader[module_name].__dict__[key],types.FunctionType)
                if builtin or dynamic:
                    name = loader[module_name].__dict__[key].__name__
                    if builtin:
                        log.debug("Function "+name+" is C")
                    if dynamic:
                        log.debug("Function "+name+" is Python")
                    try:
                        return_type=signature(loader[module_name].__dict__[key]).return_annotation
                        try:
                            data_type=signature(loader[module_name].__dict__[key]).parameters['data'].annotation
                        except:
                            data_type = None
                    except ValueError as v:
                        return_type = None
                        data_type = None
                    self[name]=(return_type,data_type)

#from stopeight.util.editor.data import ScribbleData, ScribbleBackup
class Algorithm_Run:

    @staticmethod
    def _auto_out(module_name,package_type,function_name):
        top = module_name+'.'+function_name
        import os
        sub = 'HEAD'
        from stopeight import version
        if (package_type==True):
            #get head from current directory (os.getcwd()).endswith('stopeight')
            sub=version.__dict__['_mod_version']
        else:
            #get head from stopeight-clibs
            sub=version.__dict__['_lib_version']
        top = os.path.join(top,sub)
        return top

    @staticmethod
    def run(module,currentText,inputdata=None):
        import time
        time = time.time()
        #data = ScribbleData()
        #backup = ScribbleBackup()#get singleton
        #backup[:] = data#assign copy
        outputdata=None
        try:
            if inputdata!=None:
                backup = inputdata[:]
                log.info("Invoking "+currentText+" with "+str(len(inputdata))+" inputdata sets...")
                outputdata = loader[module[0]].__dict__[currentText](inputdata)
                #if backup == outputdata:
                #    raise Exception("Backup not successful or function values unchanged")
                log.info("Size after call: Input "+str(len(backup))+", Output "+str(len(outputdata)))
            else:
                backup = None
                log.info("Invoking "+currentText+" without inputdata.")
                outputdata = loader[module[0]].__dict__[currentText]()
                log.info("Size after call: Output "+str(len(outputdata)))

        #except:
        except BaseException as e:
            log.error("Error during method invokation: "+module[0]+'.'+currentText)
            
            from stopeight.util.editor.modules import file
            from os.path import expanduser,join
            file._write(backup,time,outdir=join(expanduser("~"),_LOGDIR
                                                ,Algorithm_Run._auto_out(module[0],module[1],currentText)
                                                #,_identify(_DATA['MyScribble'])
                                                ))
            if outputdata!=None:
                del outputdata[:]
                if (len(outputdata)>0):
                    raise Exception("outputdata clear failed!")
            log.error(e)
        return outputdata
            
class Scribble_Run:

    @staticmethod
    def _identify(scribblearea):
        import os
            
        #if (os.getcwd()).endswith('stopeight'):
        #    if (self.select.module_name=='stopeight.util.editor.modules.file'):
        if hasattr(scribblearea,'tablet_id'):
            sub = str(scribblearea.tablet_id)
        else:
            sub = 'MouseData'
        return sub
    
from PyQt5.QtCore import Qt
import inspect
#def zoo(a: str)->int:
    #if (signature(zoo).return_annotation!=Signature.empty):
class Connector:
    def __init__(self,command,outputObjects):
        self._outputs = outputObjects
        self._module = command
        self.select = QComboBox()
        self.methods = Algorithm_Select(self._module)
        for method in iter(self.methods):
            self.select.addItem(method)
        self.button = QPushButton()
        self.button.setText("Run")
        self.button.clicked.connect(self.run)

    def run(self):
        functionName = self.select.currentText()
        if functionName in self.methods:
            #check return type of unique functionname
            if (self.methods[functionName])[0]==None:
                log.info("Function "+functionName+" does not support signature")
            else:
                #check all outputs for receiving __call__
                for output in self._outputs:
                #try:
                    outputentry = signature(output.__call__).parameters['data'].annotation
                    functionreturn = (self.methods[functionName])[0]
                    if functionreturn == outputentry:
                        functionentry = (self.methods[functionName])[1]
                        log.debug("Method "+str(self.methods[functionName]))
                        executed = False
                        if functionentry!=None:#data parameter found
                            if type(output.data)==functionreturn:
                                for _input in self._outputs:
                                    if type(_input.data)==functionentry:
                                        if executed:
                                            raise Exception("There are multiple objects handling "+type(_input.data)+". The \
current version does not support handling multiple Input objects of the same type. Please remove "+str(self._module)+" from module list.")
                                        log.info("Executing "+functionName+" with "+str(type(_input.data)))
                                        output(Algorithm_Run.run(self._module,functionName,inputdata=_input.data))
                                        executed = True
                                    else:
                                        log.debug("Skipping input "+str(type(input)))
                            else:
                                log.debug("Skipping output "+str(type(output)))
                        if executed==False:
                            log.info("Fallback. Trying to call "+functionName+" without data")
                            output(Algorithm_Run.run(self._module,functionName))
                                            
                #except AttributeError as ae:
                #    pass
        else:
            raise NameError("Function not found")

#class WaveConnector(Connector):
#    def __init__(self,command,scribble):
#        super().__init__(command,[WaveData()],scribble)

#    def run(self):
#        super().run()
