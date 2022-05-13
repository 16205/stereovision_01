import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import time
import jsonTools as js

#########################################################################################################
#################################   CALIRBRATION    #####################################################
#########################################################################################################
'''
methode qui retourne les caractéristiques du système nécessaires pour le traitement d'image
'''
def calibration():
    #on définit le chessboard
    number_of_square_X = 8
    number_of_square_Y = 8
    nX = number_of_square_X - 1 #le nombre de coins intérieur
    nY = number_of_square_Y - 1
    #les images sont dans le dossier configuration
    directory = "calibration"
    #on stocke les images modifiées dans un sous-dossier
    os.system('mkdir calibration/calibration_result')
    result_directory = "calibration/calibration_result"
    #creating arrays to store the object points and the image points
    objpoints = [] #3D points in the real world space
    imgpoints = [] #2D points in the image plane
    #on prépare les coordonnées dans le chessboard des angles avec pour unité les cases
    objp = np.zeros((nX*nY,3), np.float32)
    objp[:,:2] = np.mgrid[0:nX,0:nY].T.reshape(-1,2)
    #on fait une boucle for pout traiter automatiquement les images
    print(os.listdir(directory))
    for filename in os.listdir(directory):
        if filename != "calibration_result" and filename != "calibration_params.json":
            filename = directory + '/' +filename
            print(filename)
            image = cv2.imread(filename)
            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # while True:
            #     cv2.imshow('img2',gray)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break
            # Find the corners on the chessboard
            success, corners = cv2.findChessboardCorners(gray, (nY, nX), None)
            # If the corners are found by the algorithm, draw them
            if success == True:
                objpoints.append(objp)
                #on ajoute les corners à la liste
                imgpoints.append(corners)
                # Draw the corners
                cv2.drawChessboardCorners(image, (nY, nX), corners, success)
                #on écrit les images modifiées dans un fichiers afin de les voir
                new_filename = result_directory + '/'+ filename[len(directory)+1::]
                # Save the new image in the working directory
                cv2.imwrite(new_filename, image)
    print("calibration's images processing done")
    #on fait la calibration grâce à opencv
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    """
    for informations about the output of the calibration output chek :
        https://learnopencv.com/camera-calibration-using-opencv/
    """
    return mtx, dist, rvecs, tvecs, objp

#on fait le calcule de la matrice fondamentale
def crochets(v):
    v = v[:,0]
    return np.array([ [ 0,-v[2],v[1] ],[ v[2],0,-v[0] ],[ -v[1],v[0],0 ] ])

def matFondamental(camLeft,centerRight,camRight):
    
    return np.array(crochets(camLeft @ centerRight) @ camLeft @ np.linalg.pinv(camRight))


def computeMatFund(mtx, dist, rvecs, tvecs):
    #on transforme le rvecs en matrice 3x3
    #rotation matrix => convert vector to matrix
    rmatRight = cv2.Rodrigues(rvecs[1])[0] #on prend le 2 car c'est le rvec de la camera de droite pour l'image 2
    rmatLeft = cv2.Rodrigues(rvecs[0])[0] #on prend le rvec 1 car c'est le rvec de la camera de gauche pour l'image 2
    #full [R|t] matrix => add t in R 
    #on construit la matrice de rotation dans le labo 1 qui couplée à la matrice de prijection permet de faire le lien 
    #entre coordinées monde et coordonnées image
    rotMatRight = np.concatenate((rmatRight,tvecs[0]), axis=1)
    rotMatLeft = np.concatenate((rmatLeft,tvecs[0]), axis=1)
    print(rotMatLeft)
    #on construit les matrices de projection des cameras en faisant le produit des matrices de m avec celles de rotation et 
    #de transposition
    camLeft = mtx @ rotMatLeft
    camRight = mtx @ rotMatRight
    # find cx and cy for both cameras
    camWorldCenterLeft = np.linalg.inv(np.concatenate((rotMatLeft,[[0,0,0,1]]), axis=0)) @ np.transpose([[0,0,0,1]])
    camWorldCenterRight = np.linalg.inv(np.concatenate((rotMatRight,[[0,0,0,1]]), axis=0)) @ np.transpose([[0,0,0,1]])
    F = matFondamental(camRight,camWorldCenterLeft,camLeft) 
    calibration_dict = {"F": F.tolist() , "camLeft" : camLeft.tolist(), "camRight" : camRight.tolist(), "camWorldCenterLeft" : camWorldCenterLeft.tolist(), "camWorldCenterRight" : camWorldCenterRight.tolist()}
    js.buildJson("calibration", "calibration_params", calibration_dict)
    return F, camLeft, camRight, camWorldCenterLeft, camWorldCenterRight



def plotDotWorld(objp, camWorldCenterLeft, camWorldCenterRight):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    ax.scatter3D(objp[:,0],objp[:,1],objp[:,2])
    
    x,y,z,d = camWorldCenterLeft
    ax.scatter(x, y, z, c='r', marker='o')
    
    x2,y2,z2,d2 = camWorldCenterRight
    ax.scatter(x2, y2, z2 , c='g', marker='o')
    
    
    plt.show()