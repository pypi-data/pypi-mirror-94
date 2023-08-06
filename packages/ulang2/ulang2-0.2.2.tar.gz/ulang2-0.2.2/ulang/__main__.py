# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.2rc1 (tags/v3.7.2rc1:75a402a217, Dec 11 2018, 22:09:03) [MSC v.1916 32 bit (Intel)]
# Embedded file name: driver.py
import sys
from ulang.runtime.main import main

if sys.argv[0].endswith('__main__.py'):
    sys.argv[0]='python -m ulang'
main()
# okay decompiling E:\ulang\ulang-0.2.2.exe_extracted\driver.pyc
