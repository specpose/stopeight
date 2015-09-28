#!/usr/bin/env python

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
log = logSwitch.logServer()

import vectorTools
from zsiTools import *

from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
#def create_database():
storage = FileStorage('Data.fs')
db = DB(storage)
connection = db.open()
root = connection.root()
log.debug('zodb File-Database connection opened...')
import atexit
def close_database():
    db.close()
    log.debug('...zodb Database connection closed.')
atexit.register(close_database)

class DBPoint(ABCPoint):
    pass       

import persistent,transaction

class DBLine(ABCLine,persistent.Persistent):
    def __init__(self, **args):
        ABCLine.__init__(self, **args)
        if len(root.keys())>0:
            self.id = root.keys()[-1] + 1
        else:
            self.id = 1

    def store(self):
        root[self.id]=self
        transaction.commit()
        pass

    @staticmethod
    def get(key):
        try:
            return root[key]
        except:
            raise Exception('database object id %d not found'%(key))

    @staticmethod
    def getAll():
        return root.values()

    def remove(self):
        try:
            del root[self.id]
            transaction.commit()
        except Exception:
            raise Exception('Error has ocurred during deletion of id %d'%(self.id))

    @staticmethod
    def from_numpy_array(mynumpyarray):
        line = DBLine()
        for vector in mynumpyarray:
            point = DBPoint()
            point.x=int(vector[0])
            point.y=int(vector[1])
            line.add_point(point)
        return line

if __name__ == "__main__":
    # This is only being used with sql-db
    #create_database()
    pass
    
def storage_example():
    vector = DBLine.from_numpy_array(array([[13,40],[50,125],[80,61],[123,79],[191,11]]))
    vector.store()
    for dbrecord in DBLine.getAll():
        print dbrecord.to_numpy_array()

