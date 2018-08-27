from PyQt5.QtWidgets import QWidget,QTextEdit,QVBoxLayout


from stopeight.logging import logSwitch
log = logSwitch.logPrint()

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
        self.f = io.BytesIO()

    #def __call__(self,data=None):
    #    with stdout_redirector(self.f):
    #        print('foobar')
    #        print(12)
    #        #libc.puts(b'this comes from C')
    #        os.system('echo and this is from echo')
    #__call__.__annotations__ = {'data': funcsigs._empty}
    
    def update(self):
        print('From callwindow: "{0}"'.format(self.f.getvalue().decode('utf-8')))
        self.text.setText(self.f.getvalue().decode('utf-8'))
        self.show()
        self.f.close()
        self.f = io.BytesIO()
