import numpy as np
from pyueye import ueye
import cv2
from lego_api import CameraApi

# Variables
# Threshold values for the blue brick
blue_lowH = 70
blue_highH = 135

blue_lowS = 0
blue_highS = 246

blue_lowV = 0
blue_highV = 255

# Threshold values for the green brick
green_lowH = 35
green_highH = 65

green_lowS = 141
green_highS = 211

green_lowV = 0
green_highV = 157

# Threshold values for the red brick
red_lowH = 0
red_highH = 7

red_lowS = 0
red_highS = 255

red_lowV = 0
red_highV = 255

# Morphology Kernel
generalKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))


def nothing(x):
    pass

def frameMorph(kernel, frameOriginal, frameToBeMorphed, morphologyMethod):
    maskMorph = cv2.morphologyEx(frameToBeMorphed, morphologyMethod, kernel)
    # resultMorph = cv2.bitwise_and(frameOriginal, frameOriginal, mask = maskMorph)
    # cv2.imshow('Frame and Blue Mask', resultMorph)
    return maskMorph

def frameThreshold(frame, HSVFrame):
    #Get the trackbar position
    #Blue brick
    blue_lowH = cv2.getTrackbarPos('Low Hue', 'Blue Control')
    blue_highH = cv2.getTrackbarPos('High Hue', 'Blue Control')

    blue_lowS = cv2.getTrackbarPos('Low Saturation', 'Blue Control')
    blue_highS = cv2.getTrackbarPos('High Saturation', 'Blue Control')

    blue_lowV = cv2.getTrackbarPos('Low Intensity', 'Blue Control')
    blue_highV = cv2.getTrackbarPos('High Intensity', 'Blue Control')

    #Green brick
    green_lowH = cv2.getTrackbarPos('Low Hue', 'Green Control')
    green_highH = cv2.getTrackbarPos('High Hue', 'Green Control')

    green_lowS = cv2.getTrackbarPos('Low Saturation', 'Green Control')
    green_highS = cv2.getTrackbarPos('High Saturation', 'Green Control')

    green_lowV = cv2.getTrackbarPos('Low Intensity', 'Green Control')
    green_highV = cv2.getTrackbarPos('High Intensity', 'Green Control')

    #Red brick
    red_lowH = cv2.getTrackbarPos('Low Hue', 'Red Control')
    red_highH = cv2.getTrackbarPos('High Hue', 'Red Control')

    red_lowS = cv2.getTrackbarPos('Low Saturation', 'Red Control')
    red_highS = cv2.getTrackbarPos('High Saturation', 'Red Control')

    red_lowV = cv2.getTrackbarPos('Low Intensity', 'Red Control')
    red_highV = cv2.getTrackbarPos('High Intensity', 'Red Control')

    #Create 2 arrays that consist of the low- and high trackbar positions. These are to be used to threshold the HSV image for the specific color
    #Blue brick
    lower_blue = np.array([blue_lowH, blue_lowS, blue_lowV])
    upper_blue = np.array([blue_highH, blue_highS, blue_highV])
    
    #Green brick
    lower_green = np.array([green_lowH, green_lowS, green_lowV])
    upper_green = np.array([green_highH, green_highS, green_highV])

    #Red brick
    lower_red = np.array([red_lowH, red_lowS, red_lowV])
    upper_red = np.array([red_highH, red_highS, red_highV])

    #Apply a Gaussian blur that has 11x11 kernel size to the HSV frame 
    HSVFrame = cv2.GaussianBlur(HSVFrame, (11, 11), 0)

    #Threshold the HSV image to create a mask that is the values within the threshold range
    blueMask = cv2.inRange(HSVFrame, lower_blue, upper_blue)
    greenMask = cv2.inRange(HSVFrame, lower_green, upper_green)
    redMask = cv2.inRange(HSVFrame, lower_red, upper_red)

    blueMaskMorph = frameMorph(generalKernel, frame, blueMask, cv2.MORPH_CLOSE)
    greenMaskMorph = frameMorph(generalKernel, frame, greenMask, cv2.MORPH_CLOSE)
    redMaskMorph = frameMorph(generalKernel, frame, redMask, cv2.MORPH_CLOSE)

    #Composite mask
    brMask = blueMaskMorph + redMaskMorph
    finalMask = brMask + greenMaskMorph
    compResult = cv2.bitwise_and(frame, frame, mask = finalMask)

    # Perform Blob Analysis
    # blubeBlobs2x2 = blobAnalysis(blueMaskMorph, 5000, 8000, 'blue', '2x2')
    blueBlobs2x4 = blobAnalysis(blueMaskMorph, 3300, 3600, 'blue', '2x4')
    # greenBlobs2x2 = blobAnalysis(greenMaskMorph, 100, 8000, 'green', '2x2')
    greenBlobs2x4 = blobAnalysis(greenMaskMorph, 3300, 3600, 'green', '2x4')
    # redBlobs2x2 = blobAnalysis(redMaskMorph, 5000, 8000, 'red', '2x2')
    redBlobs2x4 = blobAnalysis(redMaskMorph, 3300, 3600, 'red', '2x4')


    # Result of all 'rings' that are to be drawn around each of the BLOBs
    finalNumberOfBlobs = blueBlobs2x4 + redBlobs2x4 + greenBlobs2x4 #+ blubeBlobs2x2 + greenBlobs2x2 + greenBlobs2x4 + redBlobs2x2 + 
 
    #Show... Change the second argument to the blue/green/redResultMorph variables to show the result with morphology
    # cv2.imshow('Blue Color Mask', blueBlobs2x4)
    cv2.imshow('Blue Color Mask old', blueMaskMorph)
    cv2.imshow('Green Color Mask', greenMaskMorph)
    cv2.imshow('Red Color Mask', redMaskMorph)
    
    n_white_pix = np.sum(redMaskMorph == 255)
    
    print(n_white_pix)
            

    frameWithKeypoints = cv2.drawKeypoints(compResult, finalNumberOfBlobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('Composite Frame', frameWithKeypoints)

def colorTrackbars():
    #Create trackbars for color thresholding
    #Blue brick
    cv2.namedWindow('Blue Control', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Low Hue', 'Blue Control', blue_lowH, 179, nothing)
    cv2.createTrackbar('High Hue', 'Blue Control', blue_highH, 179, nothing)

    cv2.createTrackbar('Low Saturation', 'Blue Control', blue_lowS, 255, nothing)
    cv2.createTrackbar('High Saturation', 'Blue Control', blue_highS, 255, nothing)

    cv2.createTrackbar('Low Intensity', 'Blue Control', blue_lowV, 255, nothing)
    cv2.createTrackbar('High Intensity', 'Blue Control', blue_highV, 255, nothing)

    #Green brick
    cv2.namedWindow('Green Control', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Low Hue', 'Green Control', green_lowH, 179, nothing)
    cv2.createTrackbar('High Hue', 'Green Control', green_highH, 179, nothing)

    cv2.createTrackbar('Low Saturation', 'Green Control', green_lowS, 255, nothing)
    cv2.createTrackbar('High Saturation', 'Green Control', green_highS, 255, nothing)

    cv2.createTrackbar('Low Intensity', 'Green Control', green_lowV, 255, nothing)
    cv2.createTrackbar('High Intensity', 'Green Control', green_highV, 255, nothing)

    #Red brick
    cv2.namedWindow('Red Control', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Low Hue', 'Red Control', red_lowH, 179, nothing)
    cv2.createTrackbar('High Hue', 'Red Control', red_highH, 179, nothing)

    cv2.createTrackbar('Low Saturation', 'Red Control', red_lowS, 255, nothing)
    cv2.createTrackbar('High Saturation', 'Red Control', red_highS, 255, nothing)

    cv2.createTrackbar('Low Intensity', 'Red Control', red_lowV, 255, nothing)
    cv2.createTrackbar('High Intensity', 'Red Control', red_highV, 255, nothing)

def blobAnalysis(frame, minArea, maxArea, color, typeOfBrick):
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.filterByColor = True
    params.blobColor = 255

    params.filterByArea = True
    params.minArea = minArea
    params.maxArea = maxArea
    
    blobDetector = cv2.SimpleBlobDetector_create(params)
    keypoints = blobDetector.detect(frame)
    # frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    if(len(keypoints) > 0):
        print('Number of ' + str(color) + ' ' + str(typeOfBrick) + ' Bricks: ' + str(len(keypoints)))

    return keypoints



def main_loop():

    colorTrackbars()
    while(CameraApi.nRet == ueye.IS_SUCCESS):

        # In order to display the image in an OpenCV window we need to...
        # ...extract the data of our image memory
        array = ueye.get_data(CameraApi.pcImageMemory, CameraApi.width, CameraApi.height, CameraApi.nBitsPerPixel, CameraApi.pitch, copy=False)

        # bytes_per_pixel = int(nBitsPerPixel / 8)

        # ...reshape it in an numpy array...
        frame = np.reshape(array,(CameraApi.height.value, CameraApi.width.value, CameraApi.bytes_per_pixel))

        # ...resize the image by a half
        frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
        
    #---------------------------------------------------------------------------------------------------------------------------------------
        #Include image data processing here
        frame2BGR = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        HSVFrame = cv2.cvtColor(frame2BGR, cv2.COLOR_BGR2HSV)
        frameThreshold(frame2BGR, HSVFrame)
    #---------------------------------------------------------------------------------------------------------------------------------------

        #...and finally display it
        cv2.imshow("TEST", HSVFrame)

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