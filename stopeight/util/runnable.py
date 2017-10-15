import os,sys
exec_dir = os.path.abspath(os.path.join(os.getcwd(),os.pardir))
file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
if (exec_dir==file_dir):
    raise Exception("This script should not be run from inside the module's directories.")
