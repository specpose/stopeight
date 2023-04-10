from PySide2.QtWidgets import QDockWidget,QTextEdit,QVBoxLayout,QGroupBox
from PySide2.QtCore import Qt, QSize
from stopeight.util.editor.runnable import EditorApp

import sys
import os
import io

class outwindow(QDockWidget):
    def __init__(self,parent=EditorApp().window):
        super(outwindow,self).__init__("LogWindow",parent)
        self.setMinimumSize(QSize(30, 0))

        self.text = QTextEdit()
        self.setWidget(self.text)
        self.text.setText("")
        self.data = None
        self.f = io.StringIO()

    #from contextlib import redirect_stdout
    #def __call__(self,data=None):
    #    with redirect_stdout(self.f)
    #        print('foobar')
    #        print(12)
    #        #libc.puts(b'this comes from C')
    #        os.system('echo and this is from echo')
    
    def update(self):
        self.text.setText(self.f.getvalue())
        self.show()
        self.f.close()
        self.f = io.StringIO()
