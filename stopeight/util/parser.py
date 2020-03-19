#!/usr/bin/env python

# Copyright (C) 2017 Fassio Blatter

from stopeight.util import tableau_printer
import os
import numpy

import stopeight.logging as log
log.basicConfig(level=log.DEBUG,force=True)

def find_files(dir_path,suffix='.npy',base_dir=os.getcwd()):
    dir_path = os.path.join(base_dir,dir_path)
    paths = []
    if os.path.isdir(dir_path):
        log.debug('Parsing directory ' + dir_path)
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith(suffix):
                    final_path = os.path.join(root,f)
                    paths.append(final_path)
    else:
        raise Exception('Path ' + dir_path + ' is not a directory under ' + os.getcwd())
    return paths

def process_directory(dir_path,suffix,file_adapter,analyzer,base_dir=os.getcwd(),filename=None,drawResize=True):
    if type(filename) is str:
        tprinter = tableau_printer.tPrinter(filename,6)
    lines = []
    files = find_files(dir_path,suffix,base_dir)
    count = 0
    for final_path in files:
        log.info('Loading file ' + final_path + '... ')
        try:
            graph = file_adapter(final_path)
            count+=1
            if type(filename) is str:
                tprinter.draw(graph,drawResize)
            try:
                points = analyzer(graph)
                if type(filename) is str:
                    tprinter.draw(points,drawResize)
                try:
                    lines.append(numpy.array(points))
                except:
                    log.info('Cast from Analyzer Failed')
                log.info('Success')
            except:
                log.info('Analyzer Failed')
                if type(filename) is str:
                    tprinter.text('#' + str(count) + str(final_path) + ' parser failed.')
        except:
            log.info('Loading Failed')
    if type(filename) is str:
        tprinter.text('Extracted ' + str(len(lines)) + ' Comparator lines out of ' + str(count) + ' readable Graph files.')
        tprinter.write()
    return lines
