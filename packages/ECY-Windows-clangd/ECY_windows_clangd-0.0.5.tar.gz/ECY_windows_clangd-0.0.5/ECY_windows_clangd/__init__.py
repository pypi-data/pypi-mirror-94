import os

exe_path = os.path.dirname(os.path.realpath(__file__))
exe_path = exe_path.replace('\\', '/')
exe_path = exe_path + '/clangd_files/bin/clangd.exe'
