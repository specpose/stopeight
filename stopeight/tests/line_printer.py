import os
from stopeight.util.TCT_printer import TCTPrinter

if __name__=='__main__':
    import os
    print(os.getcwd())
    from stopeight import legacy
    myprinter = TCTPrinter('line_printer2.out')
    fileline = legacy.parse_file('../stopeight-clibs/legacy/tests.local/stage3-build04-authWorking/almostStraightLeg.sp')
    myprinter.lines(fileline)
    fileline = legacy.stroke_sequential(fileline)
    fileline = legacy.TCT_to_bezier(fileline)
    myprinter.TCTs(fileline)
    myprinter.write()
