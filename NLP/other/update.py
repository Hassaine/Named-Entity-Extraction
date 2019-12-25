import os
import sys
import glob

liste=glob.glob('*.py')
liste=[el.replace(".py","") for el in liste]
listeui=glob.glob('*.ui')
listeui=[el.replace(".ui","") for el in listeui]
os.system("copy *.py *_dup.py")
for filee in listeui:
    
    os.system("pyuic5 -x "+filee+".ui -o "+filee+".py")



