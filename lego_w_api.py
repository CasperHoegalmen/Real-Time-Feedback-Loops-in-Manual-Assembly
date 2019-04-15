import numpy as np
from pyueye import ueye
import cv2
import sys

#Variables
hCam = ueye.HIDS(0)             #0: first available camera;  1-254: The camera with the specified camera ID
sInfo = ueye.SENSORINFO()
cInfo = ueye.CAMINFO()
pcImageMemory = ueye.c_mem_p()
MemID = ueye.int()
rectAOI = ueye.IS_RECT()
pitch = ueye.INT()
nBitsPerPixel = ueye.INT(24)    #24: bits per pixel for color mode; take 8 bits per pixel for monochrome
channels = 3                    #3: channels for color mode(RGB); take 1 channel for monochrome
m_nColorMode = ueye.INT()		# Y8/RGB16/RGB24/REG32
bytes_per_pixel = int(nBitsPerPixel / 8)

#Threshold values for the blue brick
blue_lowH = 97
blue_highH = 134

blue_lowS = 130
blue_highS = 246

blue_lowV = 116
blue_highV = 255

#Threshold values for the green brick
green_lowH = 39
green_highH = 97

green_lowS = 150
green_highS = 255

green_lowV = 93
green_highV = 255

#Threshold values for the red brick
red_lowH = 0
red_highH = 4

red_lowS = 227
red_highS = 255

red_lowV = 0
red_highV = 210

generalKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))

#---------------------------------------------------------------------------------------------------------------------------------------
print("START")
print()


# Starts the driver and establishes the connection to the camera
nRet = ueye.is_InitCamera(hCam, None)
if nRet != ueye.IS_SUCCESS:
    print("is_InitCamera ERROR")

# Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
nRet = ueye.is_GetCameraInfo(hCam, cInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetCameraInfo ERROR")

# You can query additional information about the sensor type used in the camera
nRet = ueye.is_GetSensorInfo(hCam, sInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetSensorInfo ERROR")

nRet = ueye.is_ResetToDefault( hCam)
if nRet != ueye.IS_SUCCESS:
    print("is_ResetToDefault ERROR")

# Set display mode to DIB
nRet = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)

# Set the right color mode
if int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
    # setup the color depth to the current windows setting
    ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_BAYER: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

# elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
#     # for color camera models use RGB32 mode
#     m_nColorMode = ueye.IS_CM_BGRA8_PACKED
#     nBitsPerPixel = ueye.INT(32)
#     bytes_per_pixel = int(nBitsPerPixel / 8)
#     print("IS_COLORMODE_CBYCRY: ", )
#     print("\tm_nColorMode: \t\t", m_nColorMode)
#     print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
#     print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
#     print()

# elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
#     # for color camera models use RGB32 mode
#     m_nColorMode = ueye.IS_CM_MONO8
#     nBitsPerPixel = ueye.INT(8)
#     bytes_per_pixel = int(nBitsPerPixel / 8)
#     print("IS_COLORMODE_MONOCHROME: ", )
#     print("\tm_nColorMode: \t\t", m_nColorMode)
#     print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
#     print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
#     print()

else:
    # for monochrome camera models use Y8 mode
    m_nColorMode = ueye.IS_CM_MONO8
    nBitsPerPixel = ueye.INT(8)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("else")

# Can be used to set the size and position of an "area of interest"(AOI) within an image
nRet = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
if nRet != ueye.IS_SUCCESS:
    print("is_AOI ERROR")

width = rectAOI.s32Width
height = rectAOI.s32Height

# Prints out some information about the camera and the sensor
print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
print("Maximum image width:\t", width)
print("Maximum image height:\t", height)
print()

#---------------------------------------------------------------------------------------------------------------------------------------

# Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
nRet = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, pcImageMemory, MemID)
if nRet != ueye.IS_SUCCESS:
    print("is_AllocImageMem ERROR")
else:
    # Makes the specified image memory the active memory
    nRet = ueye.is_SetImageMem(hCam, pcImageMemory, MemID)
    if nRet != ueye.IS_SUCCESS:
        print("is_SetImageMem ERROR")
    else:
        # Set the desired color mode
        nRet = ueye.is_SetColorMode(hCam, m_nColorMode)



# Activates the camera's live video mode (free run mode)
nRet = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
if nRet != ueye.IS_SUCCESS:
    print("is_CaptureVideo ERROR")

# Enables the queue mode for existing image memory sequences
nRet = ueye.is_InquireImageMem(hCam, pcImageMemory, MemID, width, height, nBitsPerPixel, pitch)
if nRet != ueye.IS_SUCCESS:
    print("is_InquireImageMem ERROR")
else:
    print("Press q to leave the programm")

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

    #Morphology - Apply whatever is needed for the current situation.
    #blueMaskMorph = cv2.morphologyEx(blueMask, cv2.MORPH_CLOSE, generalKernel)
    #greenMaskMorph = cv2.morphologyEx(greenMask, cv2.MORPH_CLOSE, kernel)
    #redMaskMorph = cv2.morphologyEx(redMask, cv2.MORPH_CLOSE, kernel)

    #Use Bitwise-AND operation to mask the original image with blue, green, and red color masks + the morphology
    #blueResultMorph = cv2.bitwise_and(frame, frame, mask = blueMaskMorph)
    #greenResultMorph = cv2.bitwise_and(frame, frame, mask = greenMaskMorph)
    #redResultMorph = cv2.bitwise_and(frame, frame, mask = redMaskMorph)

    #Use Bitwise-AND operation to mask the original image with blue, green, and red color masks
    #blueResult = cv2.bitwise_and(frame, frame, mask = blueMask)
    #greenResult = cv2.bitwise_and(frame, frame, mask = greenMask)
    #redResult = cv2.bitwise_and(frame, frame, mask = redMask)

    blueMaskMorph = frameMorph(generalKernel, frame, blueMask, cv2.MORPH_CLOSE)
    greenMaskMorph = frameMorph(generalKernel, frame, greenMask, cv2.MORPH_CLOSE)
    redMaskMorph = frameMorph(generalKernel, frame, redMask, cv2.MORPH_CLOSE)

    #Composite mask
    brMask = blueMaskMorph + redMaskMorph
    compResult = cv2.bitwise_and(frame, frame, mask = brMask)

    blubeBlobs2x2 = blobAnalysis(blueMaskMorph, 5000, 8000, 'blue', '2x2')
    blueBlobs2x4 = blobAnalysis(blueMaskMorph, 8000, 15000, 'blue', '2x4')
    greenBlobs2x2 = blobAnalysis(greenMaskMorph, 100, 8000, 'green', '2x2')
    greenBlobs2x4 = blobAnalysis(greenMaskMorph, 8000, 15000, 'green', '2x4')

    finalNumberOfBlobs = blueBlobs2x4 + blubeBlobs2x2 + greenBlobs2x2 + greenBlobs2x4 
 
    #Show... Change the second argument to the blue/green/redResultMorph variables to show the result with morphology
    # cv2.imshow('Blue Color Mask', blueBlobs2x4)
    cv2.imshow('Blue Color Mask old', blueMaskMorph)
    cv2.imshow('Green Color Mask', greenMaskMorph)
    cv2.imshow('Red Color Mask', redMaskMorph)

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

colorTrackbars()

while(nRet == ueye.IS_SUCCESS):


    # In order to display the image in an OpenCV window we need to...
    # ...extract the data of our image memory
    array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False)

    # bytes_per_pixel = int(nBitsPerPixel / 8)

    # ...reshape it in an numpy array...
    frame = np.reshape(array,(height.value, width.value, bytes_per_pixel))

    # ...resize the image by a half
    frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
    
#---------------------------------------------------------------------------------------------------------------------------------------
    #Include image data processing here

#---------------------------------------------------------------------------------------------------------------------------------------

    #...and finally display it
    frame2BGR = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    HSVFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frameThreshold(frame2BGR, HSVFrame)
    cv2.imshow("RGBA", frame)
    cv2.imshow("RGB", frame2BGR)

    # Press q if you want to end the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#---------------------------------------------------------------------------------------------------------------------------------------

# Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
ueye.is_FreeImageMem(hCam, pcImageMemory, MemID)

# Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
ueye.is_ExitCamera(hCam)

# Destroys the OpenCv windows
cv2.destroyAllWindows()

print()
print("END")