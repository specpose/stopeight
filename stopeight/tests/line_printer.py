from stopeight.util import runnable

import os
from stopeight.util.TCT_printer import TCTPrinter

if __name__=='__main__':
    from stopeight.util import runnable
    from stopeight import legacy
    myprinter = TCTPrinter('line_printer2.out')
    fileline = legacy.parse_file('stopeight-clibs/legacy/tests/stage3-build04-authWorking/almostStraightLeg.sp')
    myprinter.lines(fileline)
    fileline = legacy.stroke_sequential(fileline)
    fileline = legacy.TCT_to_bezier(fileline)
    myprinter.TCTs(fileline)
    myprinter.write()
