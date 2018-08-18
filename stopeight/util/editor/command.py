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
                            data_type = type(None)
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
    def run(module,currentText,customsubpath,inputdata=None):
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
                                                ,customsubpath
                                                ))
            if outputdata!=None:
                del outputdata[:]
                if (len(outputdata)>0):
                    raise Exception("outputdata clear failed!")
            log.error(e)
        return outputdata
    
from PyQt5.QtCore import Qt
import inspect
import funcsigs
#python3 only
#from contextlib import redirect_stdout
#both
from stopeight.util.editor.callredirector import stdout_redirector
#def zoo(a: str)->int:
    #if (signature(zoo).return_annotation!=Signature.empty):
class Connector:
    def __init__(self,command,outputObjects,logwindow):
        self.logwindow = logwindow
        self._outputs = outputObjects
        self._module = command
        self.select = QComboBox()
        self.methods = Algorithm_Select(self._module)
        for method in iter(self.methods):
            self.select.addItem(method)
        self.button = QPushButton()
        self.button.setText("Run")
        self.button.clicked.connect(self.run)

    @staticmethod
    def _execute(executed,output,_module,functionName,customsubpath,logwindow,_data):
        with stdout_redirector(logwindow.f):
            if _data != None:
                log.info("Executing "+functionName+" with "+str(type(_data)))
                computed=Algorithm_Run.run(_module,functionName,customsubpath,inputdata=_data)
            else:
                log.info("Executing "+functionName+" with without data")
                computed=Algorithm_Run.run(_module,functionName,"")
        if output!=None:
            if type(computed)!=type(output.data):
                log.warning("functionreturn "+str(type(computed))+" not equal callannotation "+str(type(output.data)))
            output(computed)
        log.debug("update logwindow")
        logwindow.update()
        return True

    def run(self):
        functionName = self.select.currentText()
        log.debug(str(self.methods))
        if functionName in self.methods:
            #check return type of unique functionname
            if (self.methods[functionName])[0]==None:
                log.info("Function "+functionName+" does not support signature")
            else:
                functionentry = (self.methods[functionName])[1]
                log.debug("Method "+str(functionName)+" has functionentry "+str(functionentry))
                #check all outputs for receiving __call__
                executed = False
                for output in self._outputs:
                #try:
                    callannotation = signature(output.__call__).parameters['data'].annotation
                    log.debug("Output has callannotation "+str(callannotation))
                    functionreturn = (self.methods[functionName])[0]
                    log.debug("Method "+str(functionName)+" has functionreturn "+str(functionreturn))
                    if functionreturn == callannotation:
                        # currently, only one input object is supported
                        # collecting data from all inputs
                        for _input in self._outputs:
                            log.debug("Type of input object data"+str(type(_input.data)))
                            #if type(_input.data)==functionentry:
                            if functionentry==type(_input.data):
                                if executed:
                                    raise Exception("There are multiple objects handling "+str(type(_input.data))+". The \
current version does not support handling multiple Input objects of the same type. Please remove "+str(type(_input))+" from module list.")
                                executed = Connector._execute(executed,output,self._module,functionName,_input.identify(),self.logwindow,_input.data)
                        if not executed and functionentry==type(None):
                            executed = Connector._execute(executed,output,self._module,functionName,"",self.logwindow,None) 
                #except AttributeError as ae:
                #    pass
        else:
            raise NameError("Function not found")
        

#class WaveConnector(Connector):
#    def __init__(self,command,scribble):
#        super().__init__(command,[WaveData()],scribble)

#    def run(self):
#        super().run()
