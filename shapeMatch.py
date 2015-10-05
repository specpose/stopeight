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
log = logSwitch.logMath()

from lineMatch import LineMatchClass

class ShapeMatchClass(LineMatchClass):
    def __init__(self, compvec, toleranceDivider=2):
        LineMatchClass.__init__(self,compvec,toleranceDivider)

    # overwrite method in lineMatch for now
    # if we don't have SubSection matching,
    # and we don't have Directional matching,
    # it's only weighted (to be implemented: align from center not start)
    # this should be weighted, noreverse
    # is unweighted, reverse at the moment
    def match(self,invec):
        comparison = invec.copy()

        log.debug(dir(LineMatchClass))
        # this is being done if not instance of SubDivision
        if not LineMatchClass.validate_data(comparison,self.reference):
            raise Exception('data validation failed')

        comparison = self.scale(comparison)

        log.debug('Comparing:')
        log.debug(comparison)
        log.debug('To:')
        log.debug(self.reference)

        # all we need from here is comparison
        log.info('Moving comparison to point 0,0')
        inAtZero = comparison.moveToZero()
        log.debug(inAtZero)

        log.info('Moving comparison reversed to point 0,0')
        reverse = comparison.reverse()
        reverseAtZero = reverse.moveToZero()
        log.debug(reverseAtZero)

        forward = LineMatchClass.align(0,1,self.reference,inAtZero)
        backward = LineMatchClass.align(0,1,self.reference,reverseAtZero)

        if LineMatchClass.compare(self.tolerance,self.reference,forward) or LineMatchClass.compare(self.tolerance,self.reference,backward):
            log.warning('We have a match!')
            return True
        else:
            log.warning('No match.')
            return False

if __name__ == "__main__":
    import vectorTools
    from numpy import array
    log = logSwitch.logPrint()
    log.info('Starting shapeMatch...')
    input = array([[20,20],[55,130],[80,60],[120,85],[200,10]]).view(vectorTools.NumpyLine)
    log.info('rendering input.svg')
    input.printVectors('input')
    dbrecord = array([[13,40],[50,125],[80,61],[123,79],[191,11]]).view(vectorTools.NumpyLine)
    log.info('rendering dbrecord.svg')
    dbrecord.printVectors('dbrecord')
    matcher = ShapeMatchClass(dbrecord)
    if matcher.match(input):
        print 'Hooray!'
