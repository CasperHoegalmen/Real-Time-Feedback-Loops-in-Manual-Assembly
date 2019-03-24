import numpy as np
import cv2

cap = cv2.VideoCapture(0)

#Threshold values for the blue brick
blue_lowH = 97
blue_highH = 134

blue_lowS = 130
blue_highS = 246

blue_lowV = 116
blue_highV = 255

#Threshold values for the green brick
green_lowH = 65
green_highH = 86

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

#Kernels for morphology. The size of them might vary depending on the different needs of the channels, hence the color specific kernels.
generalKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
blueKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
greenKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
redKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))

def nothing(x):
    pass

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

def cameraFrame():
    colorTrackbars()

    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        #Flip the frame horizontally
        frame = cv2.flip(frame, 1)
        
        #Convert the color space from BGR --> HSV
        HSVFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frameThreshold(frame, HSVFrame)

        #Show the original camera frame and the HSV converted frame
        cv2.imshow('Original Frame - HSV Frame', np.hstack((frame, HSVFrame)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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
    brMask = blueMask + greenMask
    compResult = cv2.bitwise_and(frame, frame, mask = brMask)

    blueBlobs2x4 = blobAnalysis(blueMaskMorph, 4000, 10000, 'blue', '2x4')
    greenBlobs2x2 = blobAnalysis(greenMaskMorph, 300, 3000, 'green', '2x2')

    finalNumberOfBlobs = blueBlobs2x4 + greenBlobs2x2
 
    #Show... Change the second argument to the blue/green/redResultMorph variables to show the result with morphology
    # cv2.imshow('Blue Color Mask', blueBlobs2x4)
    cv2.imshow('Blue Color Mask old', blueMaskMorph)
    cv2.imshow('Green Color Mask', greenMaskMorph)
    cv2.imshow('Red Color Mask', redMaskMorph)
    #cv2.imshow('Frame and Blue Mask', blueResult)
    #cv2.imshow('Frame and Green Mask', greenResult)
    #cv2.imshow('Frame and Red Mask', redResult)

    frameWithKeypoints = cv2.drawKeypoints(compResult, finalNumberOfBlobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('Composite Frame', frameWithKeypoints)
    

def frameMorph(kernel, frameOriginal, frameToBeMorphed, morphologyMethod):
    maskMorph = cv2.morphologyEx(frameToBeMorphed, morphologyMethod, kernel)
    # resultMorph = cv2.bitwise_and(frameOriginal, frameOriginal, mask = maskMorph)
    # cv2.imshow('Frame and Blue Mask', resultMorph)
    return maskMorph


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

cameraFrame()
# When everything done, release the capture
cv2.destroyAllWindows()
cap.release()