import calibration as cal
import image_processing as ip
import cv2
import numpy as np
from scan_processing import *


mtx, dist, rvecs, tvecs, objp = cal.calibration()
F, camLeft, camRight, camWorldCenterLeft, camWorldCenterRight = cal.computeMatFund(mtx, dist, rvecs, tvecs)

cal.plotDotWorld(objp, camWorldCenterLeft, camWorldCenterRight)
print(camWorldCenterLeft, camWorldCenterRight)
computePointCloud4Scan("test",F, camWorldCenterRight, camWorldCenterLeft, camLeft, camRight)
    
