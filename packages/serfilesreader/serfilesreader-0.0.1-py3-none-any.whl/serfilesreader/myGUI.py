# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 14:42:10 2020

@author: valer
"""

import PySimpleGUI as sg

def UI_getROI ():
    sg.theme('Dark2')
    sg.theme_button_color(('white', '#500000'))
    layout = [[sg.Text('Fenetre x1,y1,largeur, Hauteur'), 
           sg.Text(size=(10,1), key='-OUTPUT-')], 
          [sg.Input(key='-IN-',enable_events=True)], 
          [sg.Button('Ok')]] 
  
    window = sg.Window('Entrez la taille et position de la ROI', layout) 
  
    while True: 
        event, values = window.read()
      
        if event==sg.WIN_CLOSED: 
            break
        
        if event in ('Ok'):
            myEntryText= values['-IN-']
            window.close() 
        
        if event == '-IN-'and values['-IN-'] and values['-IN-'][-1] not in ('0123456789.,'):
            window['-IN-'].update(values['-IN-'][:-1])
    
    return myEntryText

def UI_BrowserFileName ():
    sg.theme('Dark2')
    sg.theme_button_color(('white', '#500000'))
    fname = sg.popup_get_file('Document to open')
    return fname

def UI_getFileName ():
    sg.theme('Dark2')
    sg.theme_button_color(('white', '#500000'))
    layout = [[sg.Text('Nom du fichier, sans extension .ser'), 
           sg.Text(size=(10,1), key='-OUTPUT-')], 
          [sg.Input(key='-IN-')], 
          [sg.Button('Ok')]] 
  
    window = sg.Window('Capture fichier video SER', layout) 
  
    while True: 
        event, values = window.read() 
        print(event, values) 
      
        if event==sg.WIN_CLOSED: 
            break
        
        if event in ('Ok'):
            # Update the "output" text element 
            # to be the value of "input" element 
            window['-OUTPUT-'].update(values['-IN-']) 
            myEntryText= values['-IN-']+".ser"
            window.close() 
    
    return myEntryText

def UI_saveFileName ():
    sg.theme('Dark2')
    sg.theme_button_color(('white', '#500000'))
    
    text = sg.PopupGetFile('Entrez nom de fichier avec bouton save as...', default_path='', default_extension='.ser', save_as=True, file_types=(("SER Files", "*.ser"),))      
    ##sg.Popup('Results', 'The value returned from PopupGetFile', text)    
    return text

def UI_getExpGain ():
    sg.theme('Dark2')
    sg.theme_button_color(('white', '#500000'))
    
    layout = [
    [sg.Text('Acquisition')],
    [sg.Text('Exposition (ms)', size=(15, 1)), sg.InputText()],
    [sg.Text('Gain', size=(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Simple data entry window', layout)
    event, values = window.read()
    window.close()
    print(event, values[0], values[1])    # the input data looks like a simple list when auto numbered
    return values

def UI_AllInOne (mytext):
    sg.theme('Dark2')
    sg.theme_button_color(('white', '#500000'))
    
    layout = [
    [sg.Text('Nom du fichier', size=(25, 1)),
     sg.InputText(default_text='c:\py\\',key='-FILE-'),
     sg.FileSaveAs(key='-SAVEAS-', file_types=(("SER Files", "*.ser"),),initial_folder='/py', default_extension='.ser')],
    [sg.Text('Fenetre x1,y1,largeur, Hauteur',size=(25,1)),
     sg.Input(size=(20,1),key='-ROI-',enable_events=True)],
    [sg.Text('Exposition (ms)', size=(25, 1)), sg.InputText(default_text='100',size=(8,1),key='-EXP-')],
    [sg.Text('Gain', size=(25,1)), sg.InputText(default_text='300',size=(18,1),key='-GAIN-')],
    [sg.Button('Video'), sg.Button('Image'),sg.Cancel()]
    ]
    
    window = sg.Window('Capture', layout, finalize=True)
    window['-ROI-'].update(mytext) 
    
    while True:
        event, values = window.read()
        
        if event==sg.WIN_CLOSED or event=='Cancel': 
            break
       
        if event == '-ROI-' and values['-ROI-'] and values['-ROI-'][-1] not in ('0123456789.,'):
            window['-ROI-'].update(values['-ROI-'][:-1])
        
        if event=='Video' or event=='Image':
            break
            
    window.close()
    
    if values['-FILE-'].lower().endswith('.ser')==False:
        values['-FILE-']=values['-FILE-']+'.ser'
               
    FileName=values['-FILE-']
    ROI=values ['-ROI-']
    Exp=values ['-EXP-']
    Gain=values ['-GAIN-']
    
    return FileName, ROI, Exp, Gain, event

def UI_SerExtractor ():
    sg.theme('Dark2')
    sg.theme_button_color(('white', '#500000'))
    
    layout = [
    [sg.Text('Nom du fichier', size=(25, 1)), sg.InputText(default_text='',size=(20,1),key='-FILE-'),
     sg.FileBrowse('Open',file_types=(("SER Files", "*.ser"),),initial_folder='/py')],
    [sg.Checkbox('Extract fichiers png', default=False, key='-FLAG-')],
    [sg.Text('fichier de sortie',size=(25,1)),sg.Input(default_text='i',size=(8,1),key='-PNG-',enable_events=True)],  
    [sg.Text('Toutes les x images', size=(25, 1)), sg.InputText(default_text='3',size=(8,1),key='-NBIMG-')],
    [sg.Button('Ok'), sg.Cancel()]
    ] 
    
    window = sg.Window('Capture', layout, finalize=True)
    
    while True:
        event, values = window.read()
        if event==sg.WIN_CLOSED or event=='Cancel': 
            break
        
        if event=='Ok':
            break
        
        if event == '-ROI-' and values['-ROI-'] and values['-ROI-'][-1] not in ('0123456789.,'):
            window['-ROI-'].update(values['-ROI-'][:-1])

    window.close()
               
    FileName=values['-FILE-']
    NamePng=values ['-PNG-']
    NbImg=values ['-NBIMG-']
    Extract=values ['-FLAG-']
    
    return FileName, NamePng, NbImg, Extract

def UI_SerFitsExtractor ():
    sg.theme('Dark2')
    sg.theme_button_color(('white', '#500000'))
    
    layout = [
    [sg.Text('Nom du fichier', size=(25, 1)), sg.InputText(default_text='',size=(20,1),key='-FILE-'),
     sg.FileBrowse('Open',file_types=(("SER Files", "*.ser"),),initial_folder='/py')],
    [sg.Text('fichier de sortie',size=(25,1)),sg.Input(default_text='s',size=(8,1),key='-PNG-',enable_events=True)],  
    [sg.Checkbox('Extract fichiers png', default=False, key='-FLAG-')],
    [sg.Text('Toutes les x images', size=(25, 1)), sg.InputText(default_text='3',size=(8,1),key='-NBIMG-')],
    [sg.Button('Ok'), sg.Cancel()]
    ] 
    
    window = sg.Window('Capture', layout, finalize=True)
    
    while True:
        event, values = window.read()
        if event==sg.WIN_CLOSED or event=='Cancel': 
            break
        
        if event=='Ok':
            break
        
        if event == '-ROI-' and values['-ROI-'] and values['-ROI-'][-1] not in ('0123456789.,'):
            window['-ROI-'].update(values['-ROI-'][:-1])

    window.close()
               
    FileName=values['-FILE-']
    NamePng=values ['-PNG-']
    NbImg=values ['-NBIMG-']
    Extract=values ['-FLAG-']
    
    return FileName, NamePng, NbImg, Extract

def UI_Ser_OnFly():
    sg.theme('Dark2')
    sg.theme_button_color(('white', '#500000'))
    
    layout = [
    [sg.Text('Nom du fichier', size=(25, 1)), sg.InputText(default_text='',size=(20,1),key='-FILE-'),
     sg.FileBrowse('Open',file_types=(("SER Files", "*.ser"),),initial_folder='/py')],
    [sg.Button('Ok'), sg.Cancel()]
    ] 
    
    window = sg.Window('Capture', layout, finalize=True)
    
    while True:
        event, values = window.read()
        if event==sg.WIN_CLOSED or event=='Cancel': 
            break
        
        if event=='Ok':
            break

    window.close()
               
    FileName=values['-FILE-']
    
    return FileName

UI_SerFitsExtractor()
