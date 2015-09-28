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
#
# Credits: This code is partially from a tutorial found on the web

from numpy import array,pi,cos,sin
from SVG import Scene
from numpy.oldnumeric.ma import dot

def idmatrix():
    return array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

def translate(a):
    m = array([[1,0,0],[0,1,0],[a[0],a[1],1]])
    return m

def scale(a):
    m = array([[a[0],0,0],[0,a[1],0],[0,0,1]])
    return m

def rotate(deg):
    if (deg!=0):
        radians = 2 * pi / (360.0/deg)
        c = cos(radians)
        s = sin(radians)
        m = array([[c,s,0],[-s,c,0],[0,0,1]])
    else:
        m = idmatrix()
    return m

def transform(a, m):
    b = array([0,0])
    b[0]= a[0] * m[0][0] + a[1]* m[1][0] + m[2][0]
    b[1]= a[0] * m[0][1] + a[1]* m[1][1] + m[2][1]
    return b

def center(a):
    return transform(a,translate(array([0,0])))

def matrixtest():
    a = array([30,30])
    m = idmatrix()
    print ('rotate vector with matrix:')
    #m = dot(translate(array([10,15])),m)
    #m = dot(scale(array([0.5,0.5])),m)
    m = dot(rotate(-90),m)
    result = transform(a,m)
    print a
    print result
    scene = Scene('matrixTools',255,255)
    scene.add(Line(center(array([0,0])),center(a)))
    scene.add(Line(center(array([0,0])),center(result)))
    scene.write_svg()
    scene.display()
    return
