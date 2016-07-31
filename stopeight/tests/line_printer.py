from stopeight.comparator.vectorTools import NumpyLine
from SVG import Scene,Line
import os

class Line(NumpyLine):
    
    def printVectors(self,filename='line_printer.out'):
        scene = Scene(filename,255,255)
        for count,v in enumerate(self[:len(self)-1]):
            scene.add(Line(center(v),center(self[count+1])))
        scene.write_svg()
        scene.display()

if __name__=='__main__':
    import stopeight_clibs_legacy
    fileline = stopeight_clibs_legacy.parse_file('./stopeight-clibs/legacy/test.local/stage3-build04-authWorking/almostStraightLeg.sp')
    print fileline
    testline = Line(fileline)
    testline.printVectors()