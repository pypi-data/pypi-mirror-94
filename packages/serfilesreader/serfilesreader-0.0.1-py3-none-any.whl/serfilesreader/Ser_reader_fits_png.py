# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 16:38:55 2020

@author: valerie
lecture fichier video ser
sauvegarde chque trame en fits
peut suaver une image sur n en png 
genere une image somme de toute les trames pour le script de traitement solex
"""
import numpy as np
#import cv2
import myGUI as sg
import os
from astropy.io import fits



#Recupere paramatres de la boite de dialogue
#
#serfile: nom du fichier ser avec repertoire et extension
#namepng: nom generique pour sauver les images de trames en png et en fits
#NbImg: sauve en png une image sur NbImg si l'option est activée
#Extract: option de sauvegarde en png d'images trame

serfile, NamePng, NbImg, Extract=sg.UI_SerFitsExtractor()
print(serfile)
WorkDir=os.path.dirname(serfile)+"/"
os.chdir(WorkDir)
base=os.path.basename(serfile)
basefich=os.path.splitext(base)[0]
print('iii', basefich, serfile)
#ouverture et lecture de l'entete du fichier ser - voir doc publique
f=open(serfile, "rb")

b=np.fromfile(serfile, dtype='int8',count=14)
print (b)
FileID=b.tobytes().decode()
print ('file ID: ',FileID)
offset=14

LuID=np.fromfile(serfile, dtype=np.uint32, count=1, offset=offset)
print (LuID[0])
offset=offset+4

ColorID=np.fromfile(serfile, dtype='uint32', count=1, offset=offset)
print(ColorID[0])
offset=offset+4

little_Endian=np.fromfile(serfile, dtype='uint32', count=1,offset=offset)
print(little_Endian[0])
offset=offset+4

Width=np.fromfile(serfile, dtype='uint32', count=1,offset=offset)
Width=Width[0]
print('Width :', Width)
offset=offset+4

Height=np.fromfile(serfile, dtype='uint32', count=1,offset=offset)
Height=Height[0]
print('Height :',Height)
offset=offset+4

PixelDepthPerPlane=np.fromfile(serfile, dtype='uint32', count=1,offset=offset)
PixelDepthPerPlane=PixelDepthPerPlane[0]
print('PixelDepth :',PixelDepthPerPlane)
offset=offset+4

FrameCount=np.fromfile(serfile, dtype='uint32', count=1,offset=offset)
FrameCount=FrameCount[0]
print('nb de frame :',FrameCount)
offset=offset+4

b=np.fromfile(serfile, dtype='int8',count=40,offset=offset)
Observer=b.tobytes().decode()
print ('Observer :',Observer)
offset=offset+40

b=np.fromfile(serfile, dtype='int8',count=40,offset=offset)
Instrument=b.tobytes().decode()
print ('Instrument :',Instrument)
offset=offset+40

b=np.fromfile(serfile, dtype='int8',count=40,offset=offset)
Telescope=b.tobytes().decode()
print ('Telescope :', Telescope)
offset=offset+40

DTime=np.fromfile(serfile, dtype='int64', count=1,offset=offset)
DTime=DTime[0]
print(DTime)
offset=offset+8

DTimeUTC=np.fromfile(serfile, dtype='int64', count=1,offset=offset)
DTimeUTC=DTimeUTC[0]
print(DTimeUTC)

#cv2.namedWindow('Ser', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('Ser', Width, Height)
#cv2.moveWindow('Ser', 100, 0)

ok_flag=True            # Flag pour sortir de la boucle de lexture avec exit
count=Width*Height       # Nombre d'octet d'une trame
FrameIndex=1             # Index de trame
offset=178               # Offset de l'entete fichier ser
sleep_interval = 0.100   # Si video tres courte permet de la ralentir
nb_image=NbImg           # NbImg vient de la boite dialogue
FileGen=WorkDir+NamePng  # Contruit le nom generique 
Index_Img=1              # Index fichier png
Ok_extract=Extract       # Flag de la boite dialogue pour sauver trames en png

#initialisation de l'entete fits des fichiers fits par trame
hdr= fits.Header()
hdr['SIMPLE']='T'
hdr['BITPIX']=32
hdr['NAXIS']=2
hdr['NAXIS1']=Width
hdr['NAXIS2']=Height
hdr['BZERO']=0
hdr['BSCALE']=1
hdr['BIN1']=1
hdr['BIN2']=1
hdr['EXPTIME']=0


#initialize le tableau qui recevra l'image somme de toutes les trames
mydata=np.zeros((Height,Width),dtype='uint64')

while FrameIndex < FrameCount and ok_flag:
    #print (FrameIndex)
    #time.sleep(sleep_interval) #pour ne pas afficher les images trop vite
    num=np.fromfile(serfile, dtype='uint16',count=count, offset=offset)
    num=np.reshape(num,(Height,Width))

    #utilistaire pour sauver en png une image sur nb_image
    if Ok_extract:
        if FrameIndex % nb_image == 0:
            FileName=FileGen+str(Index_Img)+".png"
            #on le sauve en png sur le disque
            #cv2.imwrite(FileName,num)
            Index_Img=Index_Img+1
            
   # cv2.imshow ('Ser', num)
    #if cv2.waitKey(1) == 27:                     # exit if Escape is hit
       # ok_flag=False
       
    #sauve les trames en fichier fits, nom generique FileGen
    ImgFile=FileGen+str(FrameIndex)+'.fit'
    DiskHDU=fits.PrimaryHDU(num,header=hdr)
    DiskHDU.writeto(ImgFile,overwrite=True)
    
    #ajoute les trames pour creer une image haut snr pour extraire
    #les parametres d'extraction de la colonne du centre de la raie et la
    #corriger des distorsions
    mydata=np.add(num,mydata)
    
    #increment la trame et l'offset pour lire trame suivant du fichier .ser
    FrameIndex=FrameIndex+1
    offset=178+FrameIndex*count*2
    

#cv2.destroyAllWindows()
f.close()

# calcul de l'image moyenne
myimg=mydata/(FrameIndex-1)             # Moyenne
myimg=np.array(myimg, dtype='uint16')   # Passe en entier 16 bits
AxeY=Height                             # Hauteur de l'image
AxeX=Width                              # Largeur de l'image
myimg=np.reshape(myimg, (AxeY, AxeX))   # Forme tableau X,Y de l'image moyenne
savefich=basefich+'_mean'               # Nom du fichier de l'image moyenne

# sauve en fits l'image moyenne avec suffixe _mean
SaveHdu=fits.PrimaryHDU(myimg,header=hdr)
SaveHdu.writeto(savefich+'.fit',overwrite=True)
