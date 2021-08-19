from zipfile import ZipFile
import os
from shutil import rmtree

try:
    file = open('mode.bpl')
    mode = file.readlines()[0]
    file.close()
except:
    mode = ''

if mode.strip() == 'write':
    with ZipFile('plugins.dll', 'w') as zipper:
        for i in os.listdir('data'):
            filepath = os.path.join('data', i)
            zipper.write(filepath, os.path.basename(filepath))
    rmtree('data')
elif mode.strip() == 'read':
    with ZipFile('plugins.dll', 'r') as zipper:
        for i in zipper.infolist():
            zipper.extract(i.filename, path = 'data/')
else:
    print(mode)

os.remove('mode.bpl')