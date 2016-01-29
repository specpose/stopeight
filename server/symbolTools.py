# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from stopeight.server import logSwitch
# Note: This is done depending on logging context
log = logSwitch.logServer()

import numpy
from stopeight.server.zodbTools import DBLine
from stopeight.comparator import vectorTools
from stopeight.server.zsiTools import ABCSymbol,ABCLine
from stopeight.comparator.shapeMatch import ShapeMatchClass
from stopeight.comparator.shapeMatchSubSection import ShapeMatchSubSectionClass
import time
import multiprocessing
#from stopeight.server import symbolTools
from types import NoneType

class mp_data_line():
    def __init__(self,input,dbrecord):
        self.input_line=input
        self.record_line=dbrecord.to_numpy_array().view(vectorTools.NumpyLine)
        self.record_id=dbrecord.id

def mp_match_line(next_record,results):
    counter = 0
    while 1:
        try:
            data=next_record.get(False)
        except:
            break
        counter += 1
        unweightedReverseSubSection = ShapeMatchSubSectionClass(data.record_line)
        if unweightedReverseSubSection.match(data.input_line):
            results.append((data.record_id))

class MPLine():
    def __init__(self):
        self.manager = multiprocessing.Manager()

    def __del__(self):
        self.manager.shutdown

    def matchLine(self,line,allLines):
        results = self.manager.list()

        comparison = line.to_numpy_array().view(vectorTools.NumpyLine)
#        comparison = comparison.view(dtype=numpy.dtype(float))
        log.debug('comparing %s:'%(comparison.to_tuple()))
        next_record = multiprocessing.Queue()
        for dbrecord in allLines:
            log.debug('to %s'%(dbrecord.to_tuple()))
#            dbrecord = dbrecord.view(dtype=numpy.dtype(float),type=numpy.ndarray)
            next_record.put(mp_data_line(comparison,dbrecord))
        pool = []
        for i in range(0,multiprocessing.cpu_count()): #number of CPUs plus 1
            process = multiprocessing.Process(target=mp_match_line, args=(next_record,results))
            pool.append(process)
            process.start()
        for proc in pool:
            proc.join()
        return results

    @staticmethod
    def save(line):
        if len(line.points)<=2:
            raise Exception('length of input or reference is below 3. Scale-Matching lines of size <3 is not possible.')
        # only use dbline if to be committed by session/stored or retrieved from db
        tobesaved = DBLine.from_numpy_array(line.to_numpy_array())
        tobesaved.store()
        log.info('created line id %d'%(tobesaved.id))
        return tobesaved.id

    @staticmethod
    def delete(line):
        dbline = DBLine.get(line.id)
        if (type(dbline)!=NoneType):
            # or dbline.view(matchline.ABCLine) ?
            echo = ABCLine.from_numpy_array(dbline.to_numpy_array())
            echo.id = dbline.id
            dbline.remove()
            log.info('deleted line id %d'%(line.id))
            return echo
        else:
            log.error('line id %d does not exist!'%(line.id))
            echo = ABCLine()
            echo.id = 0
            return echo

    @staticmethod
    def get(line):
        dbline = DBLine.get(line.id)
        if (type(dbline)!=NoneType):
            found = ABCLine.from_numpy_array(dbline.to_numpy_array())
            found.id = dbline.id
            log.info('retrieved line id %d'%(found.id))
            return found
        else:
            log.error('line id %d does not exist!'%(line.id))
            echo = ABCLine()
            echo.id = 0
            return echo
