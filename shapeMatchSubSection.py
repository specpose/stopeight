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

from matrixTools import *
from vectorTools import *
from shapeMatch import ShapeMatchClass

import logSwitch
log = logSwitch.logMath()

class ShapeMatchSubSectionClass:
    def __init__(self,compvec,toleranceDivider = 2):
        self.reference = compvec.copy()
        self.toleranceDivider = toleranceDivider

    # unequal length
    # multiple (instantiations) after change
    # order of vectors doesn't matter, will be flipped
    def match(self,invec):
        if (len(self.reference)<len(invec)):
            return False
            # under certain circumstances it may make sense to match a long input to a short reference
            #long = invec.copy()
            #short = self.reference.copy()
        else:
            short = invec.copy()
            long=self.reference.copy()            
        difference = len(long)-len(short)
        for count in range(difference+1):
            reordered = long.reorderToNStart(count)
            reordered = reordered[0:len(short)]
            unweightedReverse = ShapeMatchClass(short,self.toleranceDivider)
            if unweightedReverse.match(reordered):
                return True

import vectorTools
if __name__ == "__main__":
    log = logSwitch.logPrint()
    log.info('Starting shapeMatch...')
    input = array([[20,20],[55,130],[80,60],[120,85],[200,10]]).view(vectorTools.NumpyLine)
    log.info('rendering input.svg')
    input.printVectors('input')
    dbrecord = array([[5,5],[13,40],[50,125],[80,61],[123,79],[191,11],[10,10]]).view(vectorTools.NumpyLine)
    log.info('rendering dbrecord.svg')
    dbrecord.printVectors('dbrecord')
    matcher = ShapeMatchSubSectionClass(dbrecord)
    if matcher.match(input):
        print 'Hooray!'
