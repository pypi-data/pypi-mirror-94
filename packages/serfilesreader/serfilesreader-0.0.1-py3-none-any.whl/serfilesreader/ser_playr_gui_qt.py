#!/usr/bin/env python
import sys
if sys.version_info[0] >= 3:
    import PySimpleGUIQt as sg
else:
    import PySimpleGUI27 as sg
import cv2
import numpy as np
from sys import exit as exit


from serfilesreader import Serfile
print("usage : setfilesreader.py -f file.ser")


"""
Demo program that displays a webcam using OpenCV
"""
def main(filename=None):
    sg.ChangeLookAndFeel('LightGreen')
    file_choosen = True if filename != None else False
    # define the window layout
    layout = [[sg.Text('Play ser Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Text('Nom du fichier', size=(25, 1)), sg.InputText(default_text=filename if filename!= None else "" ,size=(20,1),key='-FILE-'), sg.FileBrowse('Open',file_types=(("SER Files", "*.ser"),),initial_folder='.')]  ,
              [sg.Image(filename='', key='image'),sg.Text('Frame number : ', size=(20,1), key='-NUM-')],
              [sg.Button('Play', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14'),
              sg.Button('Exit', size=(10, 1), font='Helvetica 14'),
               sg.Button('About', size=(10,1), font='Any 14')]]
    #if filename==None else [sg.Text('Nom du fichier', size=(25, 1)), sg.InputText(default_text=filename if filename!= None else "" ,size=(20,1),key='-FILE-')]
    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration - Ser Reader',
                       location=(800,400))
    window.Layout(layout)
    serfile=None

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    #cap = cv2.VideoCapture(0)
    playing = False
    
    
    
    #print(dir(sg))
    while True:
        
        event, values = window.Read(timeout=0, timeout_key='timeout')
        if event == 'Exit' or event is None:
            sys.exit(0)
            pass
        elif event == 'Play':
            playing = True
            if file_choosen : 
                #Serfile declaration
                filename=values['-FILE-']
                try :
                    if serfile==None : 
                        serfile = Serfile(filename)
                except : 
                    playing=False
                
        elif event == 'Stop':
            playing = False
            
        elif event == 'About':
            sg.PopupNoWait('Made with PySimpleGUI',
                        'www.PySimpleGUI.org',
                        'Little ser player based on serfilesreader library',
                        keep_on_top=True)
        if playing:
            #reading frame by frame
            frame, ret = serfile.read()
            if ret <0 : #end of video
                playing=False
            #resize
            
            imgbytes=cv2.imencode('.png', frame)[1].tobytes() #ditto
            window.FindElement('image').Update(data=imgbytes)
            window.FindElement('-NUM-').Update("Frame number"+str(ret))


try: 
    print("file read : ", sys.argv[2])
    fichier_ser =sys.argv[2]
except:
    fichier_ser =None
    
main(fichier_ser)
exit()
