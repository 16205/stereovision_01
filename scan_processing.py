from image_processing import *
import os
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D

# TODO json for calibration output

def computePointCloud4Scan(scan_name):
    #on construit les différentes matrices 
    calib = js.getJsonData("calibration\calibration_params.json")
    F, camLeft, camRight, camWorldCenterLeft, camWorldCenterRight = np.array(calib.get("F")), np.array(calib.get("camLeft")), np.array(calib.get("camRight")), np.array(calib.get("camWorldCenterLeft")), np.array(calib.get("camWorldCenterRight"))
    print(camWorldCenterLeft)
    #todo: remove 3tresh
    path_left_dir = scan_name + "/generated/3tresh/Left"
    path_right_dir = scan_name + "/generated/3tresh/Right"
    print(path_left_dir)
    number_pictures = len(os.listdir(path_left_dir))
    world_points = []
    points_world_dict = {"scan" : {"scan name " : scan_name}}
    for i in range(number_pictures):
        
        print(i)
        name_pict_left = path_left_dir + "/" + str(i) + ".jpg"
        name_pict_right = path_right_dir + "/" + str(i) + ".jpg"
        print(name_pict_left)

        img_left = cv2.imread(name_pict_left)
        img_right =cv2.imread(name_pict_right)

        red_pixels_img_left = getRedPixels(img_left)
        epilines_img_left = getEpilines(red_pixels_img_left, F)
        
        red_pixels_img_right = getRedPixels(img_right)

        left_right_pixels = matchLeftAndRightPixels(red_pixels_img_right, epilines_img_left, red_pixels_img_left)
        world_point_temp, worldLeft, worldRight = computeWorldCoordinates(left_right_pixels, camWorldCenterRight, camWorldCenterLeft, camLeft, camRight)
        points_world_dict.update({ i : js.serializeVectorList(world_point_temp)})
        world_points.append(world_point_temp)

    js.buildJson(scan_name, "world_coordinates(xyz)", points_world_dict)
    draw_point_cloud(world_points, worldLeft, worldRight, camWorldCenterLeft, camWorldCenterRight)


def draw_point_cloud(world_points, worldLeft, worldRight, camWorldCenterLeft, camWorldCenterRight):
    x, y, z = [], [], []
    for points in world_points:
        for point in points:
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
    figure = plt.figure()
    ax = Axes3D(figure, auto_add_to_figure=False) ## auto_add_to_figure=False pour ne plus avoir d'erreur
    figure.add_axes(ax) ## Pour ne plus avoir d'erreur
    ax.scatter(x, y, z, c='r', marker='o')
    # ax.scatter(xright, yright, zright, c='b', marker='*')
    x1,y1,z1,d = camWorldCenterLeft
    ax.scatter(x1, y1, z1 , c='g', marker='+')
    x2,y2,z2,d2 = camWorldCenterRight
    ax.scatter(x2, y2, z2 , c='b', marker='+')
    ax.scatter(0, 0, 0, c='r', marker = '*')
    ax.set_xlabel('$X$', fontsize=20, rotation=150)
    ax.set_ylabel('$Y$')
    ax.set_zlabel('$z$', fontsize=30, rotation=60)
    plt.show()





# def lineY(coefs,x):
#     a,b,c = coefs
#     return-(c+a*x)/b


# def drawEpilines(img, epilines):

#     for i in range(0, len(epilines), 80):
#         plt.plot([0,img.shape[0]],[lineY(epilines[i],0),lineY(epilines[i],img.shape[0])],'g')
#         plt.imshow(img)
#     plt.show()
        

