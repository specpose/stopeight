def test_Sequential():
    from stopeight.util.editor.modules import legacy
    from stopeight.util.parser import process_directory
    import os
    import stopeight.logging as log
    log.setLevel(log.CRITICAL)
    lines = process_directory(os.path.join('stopeight-clibs','legacy','test-data'),'.sp',legacy._parse_file,legacy.stroke_sequential,filename='Sequential.out',drawResize=False)

#def test_Parallel():
#    from stopeight.util.editor.modules import legacy
#    from stopeight.util.parser import process_directory
#    import os
#    import stopeight.logging as log
#    log.setLevel(log.CRITICAL)
#    lines = process_directory(os.path.join('stopeight-clibs','legacy','test-data'),'.sp',legacy._parse_file,legacy.stroke_parallel,filename='Parallel.out',drawResize=False)