import myGUI as sg

serfile, NamePng, NbImg, Extract=sg.UI_SerFitsExtractor()
print(serfile)
WorkDir=os.path.dirname(serfile)+"/"
os.chdir(WorkDir)
base=os.path.basename(serfile)
basefich=os.path.splitext(base)[0]
