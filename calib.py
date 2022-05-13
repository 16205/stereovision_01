# Import des dépendances nécessaires
import cv2 
import numpy as np
import glob
from matplotlib import pyplot as plt
import os

# __________________________________________CALIBRATION DES CAMERAS__________________________________________

# On définit le chessboard
# Chessboard dimensions
number_of_squares_X = 8 # Nombre de cases du chessboard le long de l'axe x
number_of_squares_Y = 8  # Nombre de cases du chessboard le long de l'axe y
nX = number_of_squares_X - 1 # Nombre de coins intérieurs le long de l'axe x
nY = number_of_squares_Y - 1 # Nombre de coins intérieurs le long de l'axe y

# On fait une boucle  for pour parcourir toutes les images du chessboard (++ sélection des images)
directory = "chessboards/test"
result_directory = "chessboards/result/"

# Prépare object points, comme (0,0,0), (1,0,0), (2,0,0) ...., (6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

# Tableaux pour stocker les points de l'objet et les points de l'image de toutes les images.
objpoints = [] # 3d point dans le monde réel
imgpoints = [] # 2d points dans le plan image
for filename in os.listdir(directory):
    filename = directory + "/" + filename
    print (filename)
    
    # Load une image
    image = cv2.imread(filename)
    
    # Convertir l'image en niveaux de gris (grayscale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
 
    # Trouver les coins du chessboard
    success, corners = cv2.findChessboardCorners(gray, (nY, nX), None)
    print(success)
     
    # Si les coins sont trouvés par l'algorithme, on les dessine.
    if success == True:
        objpoints.append(objp)
    
        # On ajoute les corners à la liste
        imgpoints.append(corners)
    
        # Dessine les corners
        cv2.drawChessboardCorners(image, (nY, nX), corners, success)
    
        # On écrit les images modifiées dans un fichiers afin de les voir
        new_filename =  result_directory + filename[len(directory)+1::]    
    
        # Save la nouvelle image dans le working directory
        cv2.imwrite(new_filename, image)
print("DONE")


# __________________________________________MATRICE DE PROJECTION__________________________________________

# On va traiter les différents corner pour créer la matrice de projection
# rvecs = vecteurs de rotation
# tvecs = vecteurs de translation
# mtx = Matrice A de la camera

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print(rvecs)
print("__________________________________________________")
print(tvecs)

# On transforme le rvecs en matrice 3x3
# Rotation matrix => Convertir un vecteur en matrice
rmatRight = cv2.Rodrigues(rvecs[3])[0] ## rvecs 3 représente c4Right
rmatLeft = cv2.Rodrigues(rvecs[2])[0] ## rvecs 2 représente c4Left
# Le 3 et le 2 correspondent aux lignes qui sont renvoyée par Rvecs et chaque ligne correspond à une image du chessboard
# Selon l'ordre dans lequel on lit les images 
print('----------')
print(cv2.Rodrigues(rvecs[3]))
print('---------')

# Full [R|t] matrix => ajout t in R
rotMatRight = np.concatenate((rmatRight,tvecs[0]), axis=1)
rotMatLeft = np.concatenate((rmatLeft,tvecs[0]), axis=1)
# Matrice caméra (A [R|t])
camLeft = mtx @ rotMatLeft
camRight = mtx @ rotMatRight
# Trouver cx et cy pour chaque caméra
camWorldCenterLeft = np.linalg.inv(np.concatenate((rotMatLeft,[[0,0,0,1]]), axis=0)) @ np.transpose([[0,0,0,1]])
camWorldCenterRight = np.linalg.inv(np.concatenate((rotMatRight,[[0,0,0,1]]), axis=0)) @ np.transpose([[0,0,0,1]])
print("DONE")


# Visualization
# _______________________Montrer tous les coins et le centre optique des caméras gauche et droite____________________

def plotDotWorld():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    ax.scatter3D(objp[:,0],objp[:,1],objp[:,2])
    
    x,y,z,d = camWorldCenterLeft
    ax.scatter(x, y, z, c='r', marker='o') ## En rouge, le centre caméra gauche
    
    x2,y2,z2,d2 = camWorldCenterRight
    ax.scatter(x2, y2, z2 , c='g', marker='o') ## En vert, le centre caméra droite
    
    plt.show()
    
plotDotWorld()
print("DONE")