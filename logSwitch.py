# matchline: Comparing sequences of points in 2 dimensions.
# Copyright (C) 2009-2012 Specific Purpose Software GmbH
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; NO OTHER VERSION than version 2.0 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import traceback
import logging

# Note: This is done once at start of server
def initialize_config():
    import logging.config
    logging.config.fileConfig('logging.conf')

def concatenate_traceback(sys):
    tb = traceback.format_exception(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2],limit=None)
    #tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
    string = '\n'
    for line in tb:
        string = string+line
    return string

# python logging module (slow)
class logServer(logging.Logger):
    def __new__(cls):
        return logging.getLogger('server')

# python logging module (slow)
class logMath(logging.Logger):
    def __new__(cls):
        return logging.getLogger('math')

# or just print to stdout (fast?)
class logPrint:

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
