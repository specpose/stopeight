# Copyright (C) 2009-2012 Specific Purpose Software GmbH

import traceback
import logging

def initialize_config():
    """ Note: Goes into corresponding __init__.py file. This is done once at import of module that needs logging.
    """
    import os
    if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)),'logging.conf')):
	import logging.config
    	logging.config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)),'logging.conf'))

def concatenate_traceback(sys):
    tb = traceback.format_exception(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2],limit=None)
    #tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
    string = '\n'
    for line in tb:
        string = string+line
    return string

# this is to overwrite previous imports of log and avoid commenting within file
class logNone:

    @staticmethod
    def debug(message):
        pass
    
    @staticmethod
    def info(message):
        pass

    @staticmethod
    def warning(message):
        pass

    @staticmethod
    def error(message):
        pass

    @staticmethod
    def critical(message):
        pass

# just print to stdout (fast?)
class logPrint:
#class logPrint(logging.getLoggerClass()):

    @staticmethod
    def debug(message):
        print "debug: ",message
    
    @staticmethod
    def info(message):
        print "info: ",message

    @staticmethod
    def warning(message):
        print "WARN: ",message

    @staticmethod
    def error(message):
        print "ERROR: ",message

    @staticmethod
    def critical(message):
        print "CRITICAL: ",message

# python logging module (slow)
# alerts
#class logServer(logging.getLoggerClass()):
# fails silently
class logServer(logNone):
    def __new__(cls):
        return logging.getLogger('server')

# python logging module (slow)
#class logMath(logging.getLoggerClass()):
# fails silently
class logMath(logNone):
    def __new__(cls):
        return logging.getLogger('math')
