import os
import cv2
import numpy as np
from PIL import Image
recognizer = cv2.face_LBPHFaceRecognizer.create()
path = r'D:\Python\Python_DA5\face_images_folder'
def getImagesWithID(path):
    imagePaths=[os.path.join(path, f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow('training', faceNp)
        cv2.waitKey(10)
    return np.array(IDs), faces

Ids, faces = getImagesWithID(path)
recognizer.train(faces, Ids)

if not os.path.exists('detect person/trainer'):
    os.makedirs('detect person/trainer')

recognizer.save("detect person/trainer/face_trainner.yml")
cv2.destroyAllWindows()
