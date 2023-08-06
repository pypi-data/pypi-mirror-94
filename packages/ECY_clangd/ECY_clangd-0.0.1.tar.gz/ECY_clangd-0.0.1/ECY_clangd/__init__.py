import sys
import importlib


def GetCurrentOS():
    temp = sys.platform
    if temp == 'win32':
        return 'windows'
    if temp == 'darwin':
        return 'mac'
    return 'linux'


clangd_version = 'ECY_%s_clangd' % (GetCurrentOS())

temp = importlib.import_module(clangd_version)

clangd_path = temp.exe_path
exe_path = temp.exe_path
