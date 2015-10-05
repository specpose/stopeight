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

import logSwitch
# Note: This is done depending on logging context
log = logSwitch.logServer()

import zsiTools
import requestProcessing

import sys

def matchLine(ABCSymbol):
    try:
        return requestProcessing.match_line(ABCSymbol.lines[0])
    except Exception:
        log.error(logSwitch.concatenate_traceback(sys))
        raise Exception

def saveLine(ABCSymbol):
    try:
        id = requestProcessing.save_line(ABCSymbol.lines[0])
        output = ABCSymbol
        # assigning new id from database
        output[0].id = id
        return output
    except Exception:
        log.error(logSwitch.concatenate_traceback(sys))
        raise Exception

def getLine(ABCSymbol):
    try:
        output = ABCSymbol
        line = requestProcessing.get_line(ABCSymbol.lines[0])
        output.lines=[]
        output.add_line(line)
        return output
    except Exception:
        log.error(logSwitch.concatenate_traceback(sys))
        raise Exception

def deleteLine(ABCSymbol):
    try:
        output = ABCSymbol
        line = requestProcessing.delete_line(ABCSymbol.lines[0])
        # assigning id of deleted line or 0 if error
        output.lines=[]
        output.add_line(line)
        return output
    except Exception:
        log.error(logSwitch.concatenate_traceback(sys))
        raise Exception

