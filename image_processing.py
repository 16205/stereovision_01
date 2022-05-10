import cv2
import numpy as np
import os
import jsonTools as js

"""
Sur les images de gauche,
on prend ligne par ligne par image et sur chaque ligne on défini le pixel du milieu du laser en faisant un moyenne pondérée
"""
def get_red_points(scan_name):
    dir_path_left = scan_name + "/generated/3tresh/Left/"
    #on crée un dico qui va receoire les coords de toute les images qu'on mettra ensuite en json
    length = len(os.listdir(dir_path_left))
    y_line = 0
    data_points = {"scan": {"scan_name": scan_name}}
    for i in range(length):
        img = cv2.imread(dir_path_left + str(i) + ".jpg")
        img = cv2.threshold()
        coords = []
        for line in img:
            x_pix = 0
            moy = 0
            count = 0
            for pixel in line:
                if pixel!=255:
                    moy = moy + x_pix
                    count += 1
                x_pix+=1
            if count != 0:
                moy = int(moy/count)
            if moy!=0:
                coord = np.array([[moy, y_line, 1]]) #on fixe le s = 1 cela fera aussi matcher les dimensions de points et de la mat fond
                coords.append(coords,coord,axis=0)
            y_line+=1
            data_points.update( {i : coords} )
    js.buildJson("test", "left_point_image", data_points)
      
print("ok")
get_red_points("test")