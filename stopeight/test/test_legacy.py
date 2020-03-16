def test_SampleData():
    from PyQt5.QtWidgets import QApplication,QMainWindow
    from stopeight.util.editor.modules import legacy
    from stopeight.util.parser import process_directory
    lines = process_directory('stopeight-clibs/legacy/tests','.sp',legacy._parse_file,legacy.stroke_sequential,draw=True,drawResize=False)