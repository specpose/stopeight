import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import Qt

class EditorWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        s = super().__init__(*args, **kwargs)
        self.setWindowTitle("Editor")

# Singleton
class EditorApp(QApplication):
    _instance=None
    window=None
    ## object.__call__ is object()(), not object() unlike type()
    def __new__(cls, *args, **kwargs):
        if cls._instance==None:
            cls._instance = super().__new__(cls,sys.argv)
            cls._instance.setAttribute(Qt.AA_CompressHighFrequencyEvents, False)
            cls._instance.setAttribute(Qt.AA_CompressTabletEvents, False)
            cls._instance.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents, False)
            cls._instance.setAttribute(Qt.AA_SynthesizeMouseForUnhandledTouchEvents, False)
            cls._instance.setAttribute(Qt.AA_SynthesizeMouseForUnhandledTabletEvents, False)
        return cls._instance
    def __init__(self, *args, **kwargs):
        if self.window==None:
            super().__init__(sys.argv)
            self.window = EditorWindow()