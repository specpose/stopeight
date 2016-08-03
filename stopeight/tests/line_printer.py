from stopeight.comparator.vectorTools import NumpyLine
from SVG import Scene,Line
import os
from stopeight.analyzer.TCT_printer import TCTPrinter

class lPrinter(TCTPrinter):
    
    def printVectors(self,filename='line_printer.out'):
        scene = Scene(filename,255,255)
        for count,v in enumerate(self[:len(self)-1]):
            scene.add(Line(center(v),center(self[count+1])))
        scene.write_svg()
        scene.display()

if __name__=='__main__':
    import os
    print(os.getcwd())
    import stopeight_clibs_legacy
    myprinter = TCTPrinter('line_printer2.out')
    fileline = stopeight_clibs_legacy.parse_file('../stopeight-clibs/legacy/tests.local/stage3-build04-authWorking/almostStraightLeg.sp')
    myprinter.lines(fileline)
    fileline = stopeight_clibs_legacy.stroke_sequential(fileline)
    fileline = stopeight_clibs_legacy.TCT_to_bezier(fileline)
    myprinter.TCTs(fileline)
    myprinter.write()