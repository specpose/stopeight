def test_comparator():
    from stopeight.util.parser import process_directory
    from stopeight import legacy
    from stopeight.multiprocessing import pooling
    lines = process_directory('stopeight-clibs/legacy/tests/','.sp',legacy.parse_file,legacy.stroke_sequential)
    comparator = pooling.MPLine(lines)
    for i,line in enumerate(lines):
        matches = comparator.matchLine(line)
        print('Line ' + str(i) + ' matched ' + str(len(matches)) + ' occurences ' + str(matches))