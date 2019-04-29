import numpy as np
from pyueye import ueye
from lego_api import CameraApi
import cv2
import imutils
from lego_brick import lego_model
from server import Connection
import sys
from random import randint

class Contours:

    cnts = []
    cX = 0
    cY = 0

    @staticmethod
    def update_contours(frame):
        canny_output = cv2.Canny(frame, 2, 2 * 2)
        Contours.cnts = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Approximate contours to polygons + get bounding rects and circles
        # Contours.cnts = imutils.grab_contours(Contours.cnts)

        # for c in Contours.cnts:
        #     # compute the center of the contour
        #     area = cv2.contourArea(c)         
        #     if area > 3000 and area < 3800:
        #         M = cv2.moments(c)
        #         if(M["m00"] != 0):
        #             Contours.cX = int(M["m10"] / M["m00"])
        #             Contours.cY = int(M["m01"] / M["m00"])

def main_loop():

    tracker = cv2.TrackerKCF_create()

    ## Select boxes
    bboxes = []
    colors = []
    loop = True
    loop1 = True


    while(CameraApi.nRet == ueye.IS_SUCCESS):

        #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # In order to display the image in an OpenCV window we need to...
        # ...extract the data of our image memory
        while loop1:
            array = ueye.get_data(CameraApi.pcImageMemory, CameraApi.width, CameraApi.height, CameraApi.nBitsPerPixel, CameraApi.pitch, copy=False)

            # bytes_per_pixel = int(nBitsPerPixel / 8)

            # ...reshape it in an numpy array...
            frame = np.reshape(array,(CameraApi.height.value, CameraApi.width.value, CameraApi.bytes_per_pixel))

            # ...resize the image by a half
            frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            cv2.imshow('CAMERA', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                loop1 = False
                break

        array = ueye.get_data(CameraApi.pcImageMemory, CameraApi.width, CameraApi.height, CameraApi.nBitsPerPixel, CameraApi.pitch, copy=False)

        # bytes_per_pixel = int(nBitsPerPixel / 8)

        # ...reshape it in an numpy array...
        frame = np.reshape(array,(CameraApi.height.value, CameraApi.width.value, CameraApi.bytes_per_pixel))

        # ...resize the image by a half
        frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        Contours.update_contours(frame_gray)

        while loop:
            # draw bounding boxes over objects
            # selectROI's default behaviour is to draw box starting from the center
            # when fromCenter is set to false, you can draw box starting from top left corner
            bbox = cv2.selectROI('MultiTracker', frame)
            # bboxes.append(Contours.cnts)
            colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            print("Press q to quit selecting boxes and start tracking")
            print("Press any other key to select next object")
            k = cv2.waitKey(0) & 0xFF
            if (k == 113):  # q is pressed
                # Specify the tracker type
                trackerType = "KCF"   
                
                # Create MultiTracker object
                multiTracker = cv2.MultiTracker_create()
                
                # Initialize MultiTracker
                
                canny_output = cv2.Canny(frame_gray, 3, 3 * 2)
                _, contours= cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours_poly = [None]*len(contours)
                boundRect = [None]*len(contours)
                centers = [None]*len(contours)
                radius = [None]*len(contours)
                for i, c in enumerate(contours):
                    contours_poly[i] = cv2.approxPolyDP(c, 3, True)
                    boundRect[i] = cv2.boundingRect(contours_poly[i])
                    centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
                    multiTracker.add(tracker, frame, boundRect[i])

                loop = False
                break
    #---------------------------------------------------------------------------------------------------------------------------------------
        
        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)
        
        # draw tracked objects
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
 
        # show frame
        cv2.imshow('MultiTracker', frame)

    #---------------------------------------------------------------------------------------------------------------------------------------

        #...and finally display it

        # Press q if you want to end the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #---------------------------------------------------------------------------------------------------------------------------------------

    # Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
    ueye.is_FreeImageMem(CameraApi.hCam, CameraApi.pcImageMemory, CameraApi.MemID)

    # Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
    ueye.is_ExitCamera(CameraApi.hCam)

    # Destroys the OpenCv windows
    cv2.destroyAllWindows()

    print()
    print("END")
    

CameraApi.initialize_camera()
main_loop()