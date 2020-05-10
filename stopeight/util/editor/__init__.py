try:
    # new location for sip
    # https://www.riverbankcomputing.com/static/Docs/PyQt5/incompatibilities.html#pyqt-v5-11
   from PyQt5 import sip
except ImportError:
    from PyQt5 import QtCore
    import sip