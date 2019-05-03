import numpy as np
import cv2
import imutils
import threading
import time
from pyueye import ueye
from lego_api import CameraApi
from lego_brick import lego_model
from lego_brick import LegoBrick
from server import Connection
#import asyncio

class Contours:
    cnts = []
    cX = 0
    cY = 0

    @staticmethod
    def update_contours(frame, min_area, max_area):
        Contours.cnts = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        Contours.cnts = imutils.grab_contours(Contours.cnts)

        for c in Contours.cnts:
            # compute the center of the contour
            area = cv2.contourArea(c)         
            if area > min_area and area < max_area:
                M = cv2.moments(c)
                if(M["m00"] != 0):
                    Contours.cX = int(M["m10"] / M["m00"])
                    Contours.cY = int(M["m01"] / M["m00"])

# Variables
# Threshold values for the blue brick
blue_low_hue = 100
blue_high_hue = 115

blue_low_sat = 135
blue_high_sat = 246

blue_low_val = 40
blue_high_val = 255

# Threshold values for the green brick
green_low_hue = 55
green_high_hue = 76

green_low_sat = 147
green_high_sat = 213

green_low_val = 18
green_high_val = 255

# Threshold values for the red brick
red_low_hue = 0
red_high_hue = 7

red_low_sat = 151
red_high_sat = 255

red_low_val = 45
red_high_val = 255

# Threshold values for the purple brick
purple_low_hue = 117
purple_high_hue = 125

purple_low_sat = 55
purple_high_sat = 246

purple_low_val = 37
purple_high_val = 255

# Threshold values for the yellow brick
yellow_low_hue = 20
yellow_high_hue = 38

yellow_low_sat = 174
yellow_high_sat = 255

yellow_low_val = 155
yellow_high_val = 255

#Feedback loop related variables
assembly_step_number = ""
integer_step_number = 0
current_brick_color = ""
brick_position = False
brick_height = False
current_shape = False
aspect_ratio = 0

#Previous frame
red_old = np.ndarray(shape=(512, 80))
red_old.dtype = np.uint8
red_old[:,:] = 0
blue_old = np.ndarray(shape=(512, 80))
blue_old.dtype = np.uint8
blue_old[:,:] = 0
green_old = np.ndarray(shape=(512, 80))
green_old.dtype = np.uint8
green_old[:,:] = 0
purple_old = np.ndarray(shape=(512, 80))
purple_old.dtype = np.uint8
purple_old[:,:] = 0
yellow_old = np.ndarray(shape=(512, 80))
yellow_old.dtype = np.uint8
yellow_old[:,:] = 0

# Morphology Kernel
general_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))

def color_trackbars():
    # Create trackbars for color thresholding
    # Blue brick
    cv2.namedWindow('Blue Control', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Low Hue', 'Blue Control', blue_low_hue, 179, nothing)
    cv2.createTrackbar('High Hue', 'Blue Control', blue_high_hue, 179, nothing)

    cv2.createTrackbar('Low Saturation', 'Blue Control', blue_low_sat, 255, nothing)
    cv2.createTrackbar('High Saturation', 'Blue Control', blue_high_sat, 255, nothing)

    cv2.createTrackbar('Low Intensity', 'Blue Control', blue_low_val, 255, nothing)
    cv2.createTrackbar('High Intensity', 'Blue Control', blue_high_val, 255, nothing)

    # Green brick
    cv2.namedWindow('Green Control', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Low Hue', 'Green Control', green_low_hue, 179, nothing)
    cv2.createTrackbar('High Hue', 'Green Control', green_high_hue, 179, nothing)

    cv2.createTrackbar('Low Saturation', 'Green Control', green_low_sat, 255, nothing)
    cv2.createTrackbar('High Saturation', 'Green Control', green_high_sat, 255, nothing)

    cv2.createTrackbar('Low Intensity', 'Green Control', green_low_val, 255, nothing)
    cv2.createTrackbar('High Intensity', 'Green Control', green_high_val, 255, nothing)

    # Red brick
    cv2.namedWindow('Red Control', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Low Hue', 'Red Control', red_low_hue, 179, nothing)
    cv2.createTrackbar('High Hue', 'Red Control', red_high_hue, 179, nothing)

    cv2.createTrackbar('Low Saturation', 'Red Control', red_low_sat, 255, nothing)
    cv2.createTrackbar('High Saturation', 'Red Control', red_high_sat, 255, nothing)

    cv2.createTrackbar('Low Intensity', 'Red Control', red_low_val, 255, nothing)
    cv2.createTrackbar('High Intensity', 'Red Control', red_high_val, 255, nothing)

    # Purple brick
    cv2.namedWindow('Purple Control', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Low Hue', 'Purple Control', purple_low_hue, 179, nothing)
    cv2.createTrackbar('High Hue', 'Purple Control', purple_high_hue, 179, nothing)

    cv2.createTrackbar('Low Saturation', 'Purple Control', purple_low_sat, 255, nothing)
    cv2.createTrackbar('High Saturation', 'Purple Control', purple_high_sat, 255, nothing)

    cv2.createTrackbar('Low Intensity', 'Purple Control', purple_low_val, 255, nothing)
    cv2.createTrackbar('High Intensity', 'Purple Control', purple_high_val, 255, nothing)

    # Yellow brick
    cv2.namedWindow('Yellow Control', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Low Hue', 'Yellow Control', yellow_low_hue, 179, nothing)
    cv2.createTrackbar('High Hue', 'Yellow Control', yellow_high_hue, 179, nothing)

    cv2.createTrackbar('Low Saturation', 'Yellow Control', yellow_low_sat, 255, nothing)
    cv2.createTrackbar('High Saturation', 'Yellow Control', yellow_high_sat, 255, nothing)

    cv2.createTrackbar('Low Intensity', 'Yellow Control', yellow_low_val, 255, nothing)
    cv2.createTrackbar('High Intensity', 'Yellow Control', yellow_high_val, 255, nothing)

def nothing(x):
    pass

def frame_threshold(frame, hsv_frame):
    global assembly_step_number
    global integer_step_number
    global current_shape
    global current_brick_color
    global brick_position
    global brick_height
    global red_old
    global blue_old
    global green_old
    global purple_old
    global yellow_old

    #Assembly step
    assembly_step_number = Connection.string_message
    if assembly_step_number != "":
        integer_step_number = int(assembly_step_number)

    # Get the trackbar position
    # Blue brick
    blue_low_hue = cv2.getTrackbarPos('Low Hue', 'Blue Control')
    blue_high_hue = cv2.getTrackbarPos('High Hue', 'Blue Control')

    blue_low_sat = cv2.getTrackbarPos('Low Saturation', 'Blue Control')
    blue_high_sat = cv2.getTrackbarPos('High Saturation', 'Blue Control')

    blue_low_val = cv2.getTrackbarPos('Low Intensity', 'Blue Control')
    blue_high_val = cv2.getTrackbarPos('High Intensity', 'Blue Control')

    #Green brick
    green_low_hue = cv2.getTrackbarPos('Low Hue', 'Green Control')
    green_high_hue = cv2.getTrackbarPos('High Hue', 'Green Control')

    green_low_sat = cv2.getTrackbarPos('Low Saturation', 'Green Control')
    green_high_sat = cv2.getTrackbarPos('High Saturation', 'Green Control')

    green_low_val = cv2.getTrackbarPos('Low Intensity', 'Green Control')
    green_high_val = cv2.getTrackbarPos('High Intensity', 'Green Control')

    #Red brick
    red_low_hue = cv2.getTrackbarPos('Low Hue', 'Red Control')
    red_high_hue = cv2.getTrackbarPos('High Hue', 'Red Control')

    red_low_sat = cv2.getTrackbarPos('Low Saturation', 'Red Control')
    red_high_sat = cv2.getTrackbarPos('High Saturation', 'Red Control')

    red_low_val = cv2.getTrackbarPos('Low Intensity', 'Red Control')
    red_high_val = cv2.getTrackbarPos('High Intensity', 'Red Control')

    #Purple brick
    purple_low_hue = cv2.getTrackbarPos('Low Hue', 'Purple Control')
    purple_high_hue = cv2.getTrackbarPos('High Hue', 'Purple Control')

    purple_low_sat = cv2.getTrackbarPos('Low Saturation', 'Purple Control')
    purple_high_sat = cv2.getTrackbarPos('High Saturation', 'Purple Control')

    purple_low_val = cv2.getTrackbarPos('Low Intensity', 'Purple Control')
    purple_high_val = cv2.getTrackbarPos('High Intensity', 'Purple Control')

    #Yellow brick
    yellow_low_hue = cv2.getTrackbarPos('Low Hue', 'Yellow Control')
    yellow_high_hue = cv2.getTrackbarPos('High Hue', 'Yellow Control')

    yellow_low_sat = cv2.getTrackbarPos('Low Saturation', 'Yellow Control')
    yellow_high_sat = cv2.getTrackbarPos('High Saturation', 'Yellow Control')

    yellow_low_val = cv2.getTrackbarPos('Low Intensity', 'Yellow Control')
    yellow_high_val = cv2.getTrackbarPos('High Intensity', 'Yellow Control')

    #Create 2 arrays that consist of the low- and high trackbar positions. These are to be used to threshold the HSV image for the specific color
    #Blue brick
    lower_blue = np.array([blue_low_hue, blue_low_sat, blue_low_val])
    upper_blue = np.array([blue_high_hue, blue_high_sat, blue_high_val])
    
    #Green brick
    lower_green = np.array([green_low_hue, green_low_sat, green_low_val])
    upper_green = np.array([green_high_hue, green_high_sat, green_high_val])

    #Red brick
    lower_red = np.array([red_low_hue, red_low_sat, red_low_val])
    upper_red = np.array([red_high_hue, red_high_sat, red_high_val])

    #Purple brick
    lower_purple = np.array([purple_low_hue, purple_low_sat, purple_low_val])
    upper_purple = np.array([purple_high_hue, purple_high_sat, purple_high_val])

    #Yellow brick
    lower_yellow = np.array([yellow_low_hue, yellow_low_sat, yellow_low_val])
    upper_yellow = np.array([yellow_high_hue, yellow_high_sat, yellow_high_val])

    #Threshold the HSV image to create a mask that is the values within the threshold range
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    purple_mask = cv2.inRange(hsv_frame, lower_purple, upper_purple)
    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

    blue_mask_morph = frame_morph(general_kernel, frame, blue_mask, cv2.MORPH_CLOSE)
    green_mask_morph = frame_morph(general_kernel, frame, green_mask, cv2.MORPH_CLOSE)
    red_mask_morph = frame_morph(general_kernel, frame, red_mask, cv2.MORPH_CLOSE)
    purple_mask_morph = frame_morph(general_kernel, frame, purple_mask, cv2.MORPH_CLOSE)
    yellow_mask_morph = frame_morph(general_kernel, frame, yellow_mask, cv2.MORPH_CLOSE)
    
    #Background subtraction of the individual channels
    red_next_frame = red_mask_morph - red_old
    blue_next_frame = blue_mask_morph - blue_old
    green_next_frame = green_mask_morph - green_old
    purple_next_frame = purple_mask_morph - purple_old
    yellow_next_frame = yellow_mask_morph - yellow_old

    n_white_red_color = np.sum(red_next_frame == 255)
    n_white_green_color = np.sum(green_next_frame == 255)  
    n_white_blue_color = np.sum(blue_next_frame == 255)
    n_white_purple_color = np.sum(purple_next_frame == 255)
    n_white_yellow_color = np.sum(yellow_next_frame == 255)

    print("RED:   ", np.sum(red_next_frame == 255))
    print("GREEN: ", np.sum(green_next_frame == 255))
    print("BLUE:  ", np.sum(blue_next_frame == 255))
    print("PURPLE:  ", np.sum(purple_next_frame == 255))
    print("YELLOW:  ", np.sum(yellow_next_frame == 255))

    #Color identification that is used in the error feedback function
    color_function(n_white_red_color, n_white_green_color, n_white_blue_color, n_white_purple_color, n_white_yellow_color)

    #Composite mask
    final_mask = red_mask_morph + green_mask_morph + blue_mask_morph + purple_mask_morph + yellow_mask_morph
    comp_result = cv2.bitwise_and(frame, frame, mask = final_mask)
    comp_result_greyscale = red_next_frame + green_next_frame + blue_next_frame + purple_next_frame + yellow_next_frame

    Contours.update_contours(comp_result_greyscale, lego_model[integer_step_number].min_area, lego_model[integer_step_number].max_area)

    # Perform Blob Analysis
    blue_blobs = blob_analysis(blue_next_frame, comp_result, lego_model[integer_step_number].min_area, lego_model[integer_step_number].max_area)
    green_blobs = blob_analysis(green_next_frame, comp_result, lego_model[integer_step_number].min_area, lego_model[integer_step_number].max_area)
    red_blobs = blob_analysis(red_next_frame, comp_result, lego_model[integer_step_number].min_area, lego_model[integer_step_number].max_area)
    purple_blobs = blob_analysis(purple_next_frame, comp_result, lego_model[integer_step_number].min_area, lego_model[integer_step_number].max_area)
    yellow_blobs = blob_analysis(yellow_next_frame, comp_result, lego_model[integer_step_number].min_area, lego_model[integer_step_number].max_area)
    
    sum_of_correct_shapes = len(blue_blobs) + len(green_blobs) + len(red_blobs) + len(purple_blobs) + len(yellow_blobs)
    if sum_of_correct_shapes == 1:
        current_shape = lego_model[integer_step_number].correct_size

    check_position(red_next_frame, green_next_frame, blue_next_frame, purple_next_frame, yellow_next_frame)

    check_height(n_white_red_color, n_white_green_color, n_white_blue_color, n_white_purple_color, n_white_yellow_color)

    # for c in Contours.cnts:
    #     x, y, w, h = cv2.boundingRect(c)
    #     print("POINT: ", x, ", ", y)
    #     print("WIDTH: ", w, "    HEIGHT: ", h)

    #print("RED: ", n_white_red_color)
    #print("GREEN: ", n_white_green_color)
    #print("BLUE: ", n_white_blue_color)

    error_feedback(integer_step_number, current_brick_color, current_shape, brick_position, brick_height)

    if lego_model[integer_step_number].correct_color == True and current_shape == True and brick_position == True and brick_height == True:
        frame_thread = threading.Thread(target = save_frames, args = (3, red_mask_morph, green_mask_morph, blue_mask_morph, purple_mask_morph, yellow_mask_morph,))
        frame_thread.start()
       
    current_shape = False
    brick_position = False
    brick_height = False
    lego_model[integer_step_number].correct_color = False

    # Result of all 'rings' that are to be drawn around each of the BLOBs
    final_number_of_blobs = blue_blobs + green_blobs + red_blobs + purple_blobs + yellow_blobs
 
    #Show... Change the second argument to the blue/green/redResultMorph variables to show the result with morphology
    # cv2.imshow('Blue Color Mask', blueBlobs2x4)
    cv2.imshow('Blue Color Mask', blue_next_frame)
    cv2.imshow('Green Color Mask', green_next_frame)
    cv2.imshow('Red Color Mask', red_next_frame)
    cv2.imshow('Purple Color Mask', purple_next_frame)
    cv2.imshow('Yellow Color Mask', yellow_next_frame)
    
    frame_with_keypoints = cv2.drawKeypoints(comp_result, final_number_of_blobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('Composite Frame', frame_with_keypoints)


def frame_morph(kernel, frame_original, frame_to_be_morphed, morphology_method):
    mask_morph = cv2.morphologyEx(frame_to_be_morphed, morphology_method, kernel)
    return mask_morph

# def check_position(pixelthreshold):
#     global brick_position
    
#     print("cX: " + str(Contours.cX) + "    cY: " + str(Contours.cY))
    
#     if(Contours.cX < lego_model[integer_step_number].position_x + pixelthreshold and Contours.cX > lego_model[integer_step_number].position_x - pixelthreshold
#      and Contours.cY < lego_model[integer_step_number].position_y + pixelthreshold and Contours.cY > lego_model[integer_step_number].position_y - pixelthreshold):
#         print("awesome. Next step!")
#         brick_position = lego_model[integer_step_number].correct_position

#     return brick_position

def check_position(red, green, blue, purple, yellow):
    global brick_position

    red = red[lego_model[integer_step_number].y: lego_model[integer_step_number].h, lego_model[integer_step_number].x: lego_model[integer_step_number].w]
    green = green[lego_model[integer_step_number].y: lego_model[integer_step_number].h, lego_model[integer_step_number].x: lego_model[integer_step_number].w]
    blue = blue[lego_model[integer_step_number].y: lego_model[integer_step_number].h, lego_model[integer_step_number].x: lego_model[integer_step_number].w]
    purple = purple[lego_model[integer_step_number].y: lego_model[integer_step_number].h, lego_model[integer_step_number].x: lego_model[integer_step_number].w]
    yellow = yellow[lego_model[integer_step_number].y: lego_model[integer_step_number].h, lego_model[integer_step_number].x: lego_model[integer_step_number].w]

    red_white_pixels = np.sum(red == 255)
    green_white_pixels = np.sum(green == 255)
    blue_white_pixels = np.sum(blue == 255)
    purple_white_pixels = np.sum(purple == 255)
    yellow_white_pixels = np.sum(yellow == 255)

    # cv2.imshow("ROI", red)

    #     if w > h:
    #         aspect_ratio = float(w)/h
    #     else:
    #         aspect_ratio = h/float(w)

    if lego_model[integer_step_number].min_area < red_white_pixels and lego_model[integer_step_number].max_area > red_white_pixels:
        brick_position = lego_model[integer_step_number].correct_position
    elif lego_model[integer_step_number].min_area < green_white_pixels and lego_model[integer_step_number].max_area > green_white_pixels:
        brick_position = lego_model[integer_step_number].correct_position
    elif lego_model[integer_step_number].min_area < blue_white_pixels and lego_model[integer_step_number].max_area > blue_white_pixels:
        brick_position = lego_model[integer_step_number].correct_position
    elif lego_model[integer_step_number].min_area < purple_white_pixels and lego_model[integer_step_number].max_area > purple_white_pixels:
        brick_position = lego_model[integer_step_number].correct_position
    elif lego_model[integer_step_number].min_area < yellow_white_pixels and lego_model[integer_step_number].max_area > yellow_white_pixels:
        brick_position = lego_model[integer_step_number].correct_position

    return brick_position

def blob_analysis(frame, comp_frame, min_area, max_area):
    global aspect_ratio
    params = cv2.SimpleBlobDetector_Params()

    # Change threshold paramters
    params.filterByColor = True
    params.blobColor = 255

    params.filterByArea = True
    params.minArea = min_area
    params.maxArea = max_area

    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False
    
    blob_detector = cv2.SimpleBlobDetector_create(params)
    keypoints = blob_detector.detect(frame)

    # for c in Contours.cnts:
    #     cv2.drawContours(comp_frame, [c], -1, (0, 255, 0), 2)
    #     cv2.circle(comp_frame, (Contours.cX, Contours.cY), 7, (255, 255, 255), -1)
    #     cv2.putText(comp_frame, "center", (Contours.cX - 20, Contours.cY - 20),
    #         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    #     x, y, w, h = cv2.boundingRect(c)
    #     if w > h:
    #         aspect_ratio = float(w)/h
    #     else:
    #         aspect_ratio = h/float(w)

        #print(aspect_ratio)
    # print("KEYPOIINTS: ", len(keypoints))
    return keypoints

def check_height(red_white, green_white, blue_white, purple_white, yellow_white):
    global brick_height

    current_brick = lego_model[integer_step_number].max_area - LegoBrick.area_range

    if red_white > 400:
        if  red_white - current_brick < 10:
            brick_height = lego_model[integer_step_number].correct_height
                        
        else:
            brick_height = True

        print(".....", red_white - current_brick, "    height is ", brick_height)
            
    if blue_white > 400:
        if blue_white - current_brick < 10:
            brick_height = lego_model[integer_step_number].correct_height
            
        else:
            brick_height = True

        print(".....", blue_white - current_brick, "    height is ", brick_height)

    if green_white > 400:
        if green_white - current_brick < 10:
            brick_height = lego_model[integer_step_number].correct_height
            
        else:
            brick_height = True

        print(".....", green_white - current_brick, "    height is ", brick_height)

    if purple_white > 400:
        if purple_white - current_brick < 10:
            brick_height = lego_model[integer_step_number].correct_height
            
        else:
            brick_height = True

        print(".....", purple_white - current_brick, "    height is ", brick_height)

    if yellow_white > 400:
        if yellow_white - current_brick < 10:
            brick_height = lego_model[integer_step_number].correct_height
            
        else:
            brick_height = True

        print(".....", yellow_white - current_brick, "    height is ", brick_height)

    return brick_height

def color_function(red, green, blue, purple, yellow):
    global current_brick_color

    if red > 400:
        current_brick_color = "Red"

    elif green > 400:
        current_brick_color = "Green"

    elif blue > 400:
        current_brick_color = "Blue"
    
    elif purple > 400:
        current_brick_color = "Purple"

    elif yellow > 400:
        current_brick_color = "Yellow"

    else: 
        current_brick_color = "No predefined color is detected"

    return current_brick_color

def error_feedback(step_number, color_to_use, shape_to_use, position, height):

    #print("Step number is ", step_number)
    #print("Color is " + color_to_use)
    #print("Shape is ", shape_to_use)

    if position == True:
        Connection.position_feedback = "Correct"
    else:
        Connection.position_feedback = "Incorrect"

    if shape_to_use == True:
        Connection.shape_feedback = "Correct"
    else:
        Connection.shape_feedback = "Incorrect"

    if color_to_use == lego_model[step_number].color:
        Connection.color_feedback = "Correct"
        lego_model[step_number].correct_color = True
    else:
        Connection.color_feedback = "Incorrect"

    if height == True:
        Connection.height_feedback = "Correct"
    else:
        Connection.height_feedback = "Incorrect"

    if position == False and shape_to_use == False and color_to_use == "No predefined color is detected" and height == False:
        Connection.shape_feedback = "Incorrect"
        Connection.color_feedback = "Incorrect"
        Connection.position_feedback = "Incorrect"
        Connection.height_feedback = "Incorrect"

def save_frames(delay, red, green, blue, purple, yellow):
    global red_old
    global blue_old
    global green_old
    global purple_old
    global yellow_old

    time.sleep(delay)

    dilation_kernel = np.ones((3,3), np.uint8)

    red_old = red
    blue_old = blue
    green_old = green
    purple_old = purple
    yellow_old = yellow

    red_old = cv2.dilate(red_old, dilation_kernel, iterations = 1)
    blue_old = cv2.dilate(blue_old, dilation_kernel, iterations = 1)
    green_old = cv2.dilate(green_old, dilation_kernel, iterations = 1)
    purple_old = cv2.dilate(purple_old, dilation_kernel, iterations = 1)
    yellow_old = cv2.dilate(yellow_old, dilation_kernel, iterations = 1)
    


def main_loop():
    color_trackbars()

    while(CameraApi.nRet == ueye.IS_SUCCESS):

        # In order to display the image in an OpenCV window we need to...
        # ...extract the data of our image memory
        array = ueye.get_data(CameraApi.pcImageMemory, CameraApi.width, CameraApi.height, CameraApi.nBitsPerPixel, CameraApi.pitch, copy=False)

        # ...reshape it in an numpy array...
        frame = np.reshape(array,(CameraApi.height.value, CameraApi.width.value, CameraApi.bytes_per_pixel))

        # ...resize the image by a half
        frame = cv2.resize(frame,(0,0), fx=0.5, fy=0.5)
  
        
     #---------------------------------------------------------------------------------------------------------------------------------------
        #Convert camera feed from BGRA to BGR
        frame_to_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        #Apply a Gaussian blur that has 11x11 kernel size to the BGR frame
        frame_to_bgr = cv2.GaussianBlur(frame_to_bgr, (5, 5), 0)

        cv2.imshow("BGR Frame", frame_to_bgr)
        
        #Convert camera feed from BGR color space to HSV color space
        hsv_frame = cv2.cvtColor(frame_to_bgr, cv2.COLOR_BGR2HSV)

        frame_threshold(frame_to_bgr, hsv_frame)
       
    #---------------------------------------------------------------------------------------------------------------------------------------

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

if __name__ == "__main__":
    t1 = threading.Thread(target = Connection.server)
    t2 = threading.Thread(target = main_loop)

    t1.start()
    t2.start()