from stopeight.comparator import NumpyLine
from SVG import Scene,Line
import os

class Line(NumpyLine):
    
    def printVectors(self,filename)):
        scene = Scene(filename,255,255)
        for count,v in enumerate(self[:len(self)-1]):
            scene.add(Line(center(v),center(self[count+1])))
        scene.write_svg()
        scene.display()
