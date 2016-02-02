from stopeight.logging import logSwitch
log = logSwitch.logNone()

import os

import stopeight_clibs_legacy

import numpy

def parse_directory(dir_path):
    lines = []
    if os.path.isdir(dir_path):
        log.debug('Parsing directory '+dir_path)
        count = 0
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith('.sp'):
                    final_path = os.path.join(root,f)
                    log.info('Loading file '+final_path+'... ')
                    try:
                        graph = stopeight_clibs_legacy.parse_file(final_path)
                        count = count+1
                        try:
                            points = stopeight_clibs_legacy.stroke_parallel(graph)
                            try:
                                lines.append(numpy.array(points))
                            except:
                                log.info('Cast from Analyzer Failed')
                            log.info('Success')
                        except:
                            log.info('Analyzer Failed')
                    except:
                        log.info('Loading Failed')
        log.debug('Extracted '+str(len(lines))+' Comparator lines out of '+str(count)+' readable Graph files.')
    else:
        raise Exception('Path '+dir_path+' is not a directory')
    return lines

from stopeight.multiprocessing import pooling

if __name__=='__main__':
    lines = parse_directory('../stopeight-clibs/legacy/tests.local/')
    comparator = pooling.MPLine(lines)
    for i,line in enumerate(lines):
        matches = comparator.matchLine(line)
        print('Line '+str(i)+' matched '+str(len(matches))+' occurences '+str(matches))
