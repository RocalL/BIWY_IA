import face_recognition
import cv2
import os, glob
import simplejson
import numpy as np
from tqdm import tqdm
import time

def getNameFile(fichier):
    img = ("%s" %fichier).split(".")
    return img

dir_name = os.path.dirname(os.path.realpath(__file__))
os.chdir("img_test")
listeFichiers=glob.glob("*.jpg")

known_face_names = []
known_face_encodings = []

loopCount = 0

for fichier in tqdm(listeFichiers):
    known_face_names.append(getNameFile(fichier)[0])
    i = face_recognition.face_encodings(face_recognition.load_image_file(fichier))[0]
    known_face_encodings.append(i)


f = open(os.path.join(dir_name,'known_face_name.txt'), 'w')
simplejson.dump(known_face_names, f)
f.close()


np.savetxt(os.path.join(dir_name,'known_face_encodings.txt'), known_face_encodings, fmt="%s")

print("The train on the " + str(len(listeFichiers)) + " data file is finish")
