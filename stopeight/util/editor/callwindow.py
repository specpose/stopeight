from PyQt5.QtWidgets import QWidget,QTextEdit,QVBoxLayout


from stopeight.logging import logSwitch
log = logSwitch.logNone()

import sys
import os
import io

#python3 only
from contextlib import redirect_stdout

class outwindow(QWidget):
    def __init__(self,*args):
        QWidget.__init__(self, *args)
        self.text = QTextEdit()
        layout = QVBoxLayout(self)
        layout.addWidget(self.text)
        self.setLayout(layout)

    def __call__(self,data):
        #buffered = os.fdopen(sys.stdout.fileno(),'r',1)
        buffered = io.StringIO()
        backup = sys.stdout
        redirect_stdout(buffered)
        #sys.stdout = buffered
        log.info(data)
        log.info("stderr readable "+str(sys.stderr.readable()))
        sys.stdout = backup
        log.info(buffered)
        #mytext=""
        #for line in buffered.readLine():
        #    mytext.append(line)
        #mytext = str(buffered.read())
        #buffered.close()
        mytext = buffered.getvalue()
        redirect_stdout(backup)
        self.text.setText(mytext)
        self.show()
