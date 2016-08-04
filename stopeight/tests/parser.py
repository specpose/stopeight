from stopeight.logging import logSwitch
log = logSwitch.logPrint()
from stopeight.analyzer import tableau_printer

import os

import stopeight_clibs_legacy

import numpy

def test(g):
    return g

def parse_directory(dir_path):
    paths = []
    if os.path.isdir(dir_path):
        log.debug('Parsing directory ' + dir_path)
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith('.sp'):
                    final_path = os.path.join(root,f)
                    paths.append(final_path)
    else:
        raise Exception('Path ' + dir_path + ' is not a directory under ' + os.getcwd())
    return paths

def process_directory(dir_path,analyzer=stopeight_clibs_legacy.stroke_parallel):
    tprinter = tableau_printer.tPrinter('parser.out',6)
    lines = []
    files = parse_directory(dir_path)
    count = 0
    for final_path in files:
        log.info('Loading file ' + final_path + '... ')
        try:
            graph = stopeight_clibs_legacy.parse_file(final_path)
            count+=1
            tprinter.draw(graph)
            try:
                #points =
                #stopeight_clibs_legacy.stroke_parallel(graph)
                points = analyzer(graph)
                tprinter.draw(points)
                try:
                    lines.append(numpy.array(points))
                except:
                    log.info('Cast from Analyzer Failed')
                log.info('Success')
            except:
                log.info('Analyzer Failed')
                #tprinter.text(f+' '+str(analyzer.__name__)+'
                #failed.')
                tprinter.text('#' + str(count) + f + ' failed.')
        except:
            log.info('Loading Failed')
    tprinter.text('Extracted ' + str(len(lines)) + ' Comparator lines out of ' + str(count) + ' readable Graph files.')
    tprinter.write()

    return lines

from stopeight.multiprocessing import pooling

if __name__ == '__main__':
    lines = process_directory('../stopeight-clibs/legacy/tests.local/',stopeight_clibs_legacy.stroke_sequential)
    comparator = pooling.MPLine(lines)
    for i,line in enumerate(lines):
        matches = comparator.matchLine(line)
        print('Line ' + str(i) + ' matched ' + str(len(matches)) + ' occurences ' + str(matches))
