from PyQt5.QtWidgets import QWidget,QTextEdit,QVBoxLayout


from stopeight.logging import logSwitch
log = logSwitch.logNone()

#python3 only
from contextlib import redirect_stdout
#both
from stopeight.util.editor.callredirector import stdout_redirector

import sys
import os
import io


import funcsigs

class outwindow(QWidget):
    def __init__(self,*args):
        QWidget.__init__(self, *args)
        self.text = QTextEdit()
        layout = QVBoxLayout(self)
        layout.addWidget(self.text)
        self.setLayout(layout)
        self.data = None

    def __call__(self,data=None):
        f = io.BytesIO()

        with stdout_redirector(f):
            print('foobar')
            print(12)
            #libc.puts(b'this comes from C')
            os.system('echo and this is from echo')
        print('Got stdout: "{0}"'.format(f.getvalue().decode('utf-8')))
        self.text.setText(f.getvalue().decode('utf-8'))
        self.show()
    __call__.__annotations__ = {'data': funcsigs._empty}
