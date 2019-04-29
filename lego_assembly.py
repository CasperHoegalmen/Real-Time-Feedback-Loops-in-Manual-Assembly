import numpy as np
import cv2
import imutils
import threading
import time
from pyueye import ueye
from lego_api import CameraApi
from lego_brick import lego_model
from server import Connection
#import asyncio

class Contours:
    cnts = []
    cX = 0
    cY = 0

    @staticmethod
    def update_contours(frame):
        Contours.cnts = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        Contours.cnts = imutils.grab_contours(Contours.cnts)

        for c in Contours.cnts:
            # compute the center of the contour
            area = cv2.contourArea(c)         
            if area > 3300 and area < 3600:
                M = cv2.moments(c)
                if(M["m00"] != 0):
                    Contours.cX = int(M["m10"] / M["m00"])
                    Contours.cY = int(M["m01"] / M["m00"])

# Variables
# Threshold values for the blue brick
blue_low_hue = 70
blue_high_hue = 135

blue_low_sat = 0
blue_high_sat = 246

blue_low_val = 0
blue_high_val = 255

# Threshold values for the green brick
green_low_hue = 35
green_high_hue = 65

green_low_sat = 141
green_high_sat = 211

green_low_val = 0
green_high_val = 157

# Threshold values for the red brick
red_low_hue = 0
red_high_hue = 7

red_low_sat = 0
red_high_sat = 255

red_low_val = 0
red_high_val = 255

#Feedback loop related variables
assembly_step_number = ""
integer_step_number = 0
current_brick_color = ""
brick_position = False
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

def nothing(x):
    pass

def frame_threshold(frame, hsv_frame):
    global assembly_step_number
    global integer_step_number
    global current_shape
    global current_brick_color
    global brick_position
    global red_old
    global blue_old
    global green_old

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

    #Threshold the HSV image to create a mask that is the values within the threshold range
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    blue_mask_morph = frame_morph(general_kernel, frame, blue_mask, cv2.MORPH_CLOSE)
    green_mask_morph = frame_morph(general_kernel, frame, green_mask, cv2.MORPH_CLOSE)
    red_mask_morph = frame_morph(general_kernel, frame, red_mask, cv2.MORPH_CLOSE)

    blue_mask_morph = cv2.erode(blue_mask_morph, np.ones((10,10), np.uint8), iterations = 1)
    green_mask_morph = cv2.erode(green_mask_morph, np.ones((10,10), np.uint8), iterations = 1)
    red_mask_morph = cv2.erode(red_mask_morph, np.ones((10,10), np.uint8), iterations = 1)
    
    #Background subtraction of the individual channels
    red_next_frame = red_mask_morph - red_old
    blue_next_frame = blue_mask_morph - blue_old
    green_next_frame = green_mask_morph - green_old

    n_white_red_color = np.sum(red_next_frame == 255)
    n_white_green_color = np.sum(green_next_frame == 255)  
    n_white_blue_color = np.sum(blue_next_frame == 255)

    #Color identification that is used in the error feedback function
    color_function(n_white_red_color, n_white_green_color, n_white_blue_color)

    #Composite mask
    blue_red_mask = blue_mask_morph + red_mask_morph
    final_mask = blue_red_mask + green_mask_morph
    comp_result = cv2.bitwise_and(frame, frame, mask = final_mask)
    comp_result_greyscale = blue_mask_morph + red_mask_morph + green_mask_morph

    Contours.update_contours(comp_result_greyscale)

    # Perform Blob Analysis
    blue_blobs_2x4 = blob_analysis(blue_next_frame, comp_result, 2000, 3600, 'blue', '2x4')
    green_blobs_2x4 = blob_analysis(green_next_frame, comp_result, 2000, 3600, 'green', '2x4')
    red_blobs_2x4 = blob_analysis(red_next_frame, comp_result, 2000, 3600, 'red', '2x4')

    sum_of_correct_shapes = len(blue_blobs_2x4) + len(green_blobs_2x4) + len(red_blobs_2x4)
    if sum_of_correct_shapes > 0 and sum_of_correct_shapes <= 5:
        current_shape = lego_model[integer_step_number].correct_size

    compare_models(5)

    error_feedback(integer_step_number, current_brick_color, current_shape, brick_position)

    if lego_model[integer_step_number].correct_color == True and current_shape == True:
        frame_thread = threading.Thread(target = save_frames, args = (2, red_mask_morph, green_mask_morph, blue_mask_morph,))
        frame_thread.start()
       
    current_shape = False
    brick_position = False
    lego_model[integer_step_number].correct_color = False

    # Result of all 'rings' that are to be drawn around each of the BLOBs
    final_number_of_blobs = blue_blobs_2x4 + green_blobs_2x4 + red_blobs_2x4 
 
    #Show... Change the second argument to the blue/green/redResultMorph variables to show the result with morphology
    # cv2.imshow('Blue Color Mask', blueBlobs2x4)
    cv2.imshow('Blue Color Mask', blue_next_frame)
    cv2.imshow('Green Color Mask', green_next_frame)
    cv2.imshow('Red Color Mask', red_next_frame)
    
    frame_with_keypoints = cv2.drawKeypoints(comp_result, final_number_of_blobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('Composite Frame', frame_with_keypoints)


def frame_morph(kernel, frame_original, frame_to_be_morphed, morphology_method):
    mask_morph = cv2.morphologyEx(frame_to_be_morphed, morphology_method, kernel)
    return mask_morph

def color_function(red, green, blue):
    global current_brick_color

    if red > 500:
        current_brick_color = "Red"

    elif green > 500:
        current_brick_color = "Green"

    elif blue > 500:
        current_brick_color = "Blue"

    else: 
        current_brick_color = "No predefined color is detected"

    return current_brick_color

def compare_models(pixelthreshold):
    global brick_position
    
    print("cX: " + str(Contours.cX) + "    cY: " + str(Contours.cY))
    
    if(Contours.cX < lego_model[integer_step_number].position_x + pixelthreshold and Contours.cX > lego_model[integer_step_number].position_x - pixelthreshold
     and Contours.cY < lego_model[integer_step_number].position_y + pixelthreshold and Contours.cY > lego_model[integer_step_number].position_y - pixelthreshold):
        print("awesome. Next step!")
        brick_position = lego_model[integer_step_number].correct_position

    return brick_position

def blob_analysis(frame, comp_frame, min_area, max_area, color, brick_type):
    global aspect_ratio
    params = cv2.SimpleBlobDetector_Params()

    # Change threshold paramters
    params.filterByColor = True
    params.blobColor = 255

    params.filterByArea = True
    params.minArea = min_area
    params.maxArea = max_area
    
    blob_detector = cv2.SimpleBlobDetector_create(params)
    keypoints = blob_detector.detect(frame)

    # if(len(keypoints) > 0):
        # print('Number of ' + str(color) + ' ' + str(brick_type) + ' Bricks: ' + str(len(keypoints)))

    for c in Contours.cnts:
        # # compute the center of the contour
        # area = cv2.contourArea(c)         
        # if area > min_area and area < max_area:
        #     M = cv2.moments(c)
        #     if(M["m00"] != 0):
        #         cX = int(M["m10"] / M["m00"])
        #         cY = int(M["m01"] / M["m00"])

        #     position(cX, cY, 325, 254)
        
        # draw the contour and center of the shape on the image
        cv2.drawContours(comp_frame, [c], -1, (0, 255, 0), 2)
        cv2.circle(comp_frame, (Contours.cX, Contours.cY), 7, (255, 255, 255), -1)
        cv2.putText(comp_frame, "center", (Contours.cX - 20, Contours.cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
        x, y, w, h = cv2.boundingRect(c)
        if w > h:
            aspect_ratio = float(w)/h
        else:
            aspect_ratio = h/float(w)

        #print(aspect_ratio)

    return keypoints

def error_feedback(step_number, color_to_use, shape_to_use, position):

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

    if position == False and shape_to_use == False and color_to_use == "No predefined color is detected":
        Connection.shape_feedback = "Incorrect"
        Connection.color_feedback = "Incorrect"
        Connection.position_feedback = "Incorrect"

def save_frames(delay, red, green, blue):
    global red_old
    global blue_old
    global green_old

    time.sleep(delay)

    dilation_kernel = np.ones((3,3), np.uint8)

    red_old = red
    blue_old = blue
    green_old = green

    red_old = cv2.dilate(red_old, dilation_kernel, iterations = 1)
    blue_old = cv2.dilate(blue_old, dilation_kernel, iterations = 1)
    green_old = cv2.dilate(green_old, dilation_kernel, iterations = 1)
    


def main_loop():
    #first_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    color_trackbars()

    while(CameraApi.nRet == ueye.IS_SUCCESS):

        #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # In order to display the image in an OpenCV window we need to...
        # ...extract the data of our image memory
        array = ueye.get_data(CameraApi.pcImageMemory, CameraApi.width, CameraApi.height, CameraApi.nBitsPerPixel, CameraApi.pitch, copy=False)

        # bytes_per_pixel = int(nBitsPerPixel / 8)

        # ...reshape it in an numpy array...
        frame = np.reshape(array,(CameraApi.height.value, CameraApi.width.value, CameraApi.bytes_per_pixel))

        # ...resize the image by a half
        frame = cv2.resize(frame,(0,0), fx=0.5, fy=0.5)

        


        # if counter == counter_Plus_One:
        #    prev_frame = frame
        #    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        #    cv2.imshow("prevFrame", prev_frame)
        #    counter_Plus_One = counter + 1

        
        # if counter > 0 :
        #     difference = cv2.absdiff(prev_frame, gray_frame)
        #     ret, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        #     img[difference == 255] = [0,0,0]
        #     cv2.imshow("prev_frame", prev_frame)
        #     cv2.imshow("difference", difference)
            
      #  if counter != 0:
       #     cv2.subtract(frame, prev_frame, frame)
        
        
        
     #---------------------------------------------------------------------------------------------------------------------------------------
        #Convert camera feed from BGRA to BGR
        frame_to_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        #Apply a Gaussian blur that has 11x11 kernel size to the BGR frame
        frame_to_bgr = cv2.GaussianBlur(frame_to_bgr, (11, 11), 0)
        
        #Convert camera feed from BGR color space to HSV color space
        hsv_frame = cv2.cvtColor(frame_to_bgr, cv2.COLOR_BGR2HSV)

        frame_threshold(frame_to_bgr, hsv_frame)

        # hsv_frame = cv2.cvtColor(frame_to_bgr, cv2.COLOR_BGR2HSV)
        # hsv_frame = cv2.GaussianBlur(hsv_frame, (11, 11), 0)

        # b_original, g_original, r_original, a = cv2.split(frame)
        # b_BGRA2BGR, g_BGRA2BGR, r_BGRA2BGR = cv2.split(frame_to_bgr)

        # h, s, v = cv2.split(hsv_frame)
        # h_blur, s_blur, v_blur = cv2.split(hsv_frame2)

        # hsv_frame_without_s = cv2.merge((h, v, v))

        # cv2.imshow('HSV', hsv_frame)

        # H = hsv_frame.copy()
        # H[:, :, 1] = 0
        # H[:, :, 2] = 0
        # H = cv2.cvtColor(H, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('only H', H)

        # S = hsv_frame.copy()
        # S[:, :, 0] = 0
        # S[:, :, 2] = 0
        # S = cv2.cvtColor(S, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('only S', S)

        # V = hsv_frame.copy()
        # V[:, :, 0] = 0
        # V[:, :, 1] = 0
        # V = cv2.cvtColor(V, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('only V', V)

        
    #---------------------------------------------------------------------------------------------------------------------------------------

        #...and finally display it
        
        # cv2.imshow("HSV TEST", hsv_frame)

        # Press q if you want to end the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # cv2.imwrite("b_original.png",b_original, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            # cv2.imwrite("g_original.png",g_original, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            # cv2.imwrite("r_original.png",r_original, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

            # cv2.imwrite("b_BGRA2BGR.png",b_BGRA2BGR, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            # cv2.imwrite("g_BGRA2BGR.png",g_BGRA2BGR, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            # cv2.imwrite("r_BGRA2BGR.png",r_BGRA2BGR, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

            # cv2.imwrite("h.png",h, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            # cv2.imwrite("s.png",s, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            # cv2.imwrite("v.png",v, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

            # cv2.imwrite("h_blur.png",h_blur, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            # cv2.imwrite("s_blur.png",s_blur, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            # cv2.imwrite("v_blur.png",v_blur, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

            # cv2.imwrite("HSV_blurred_full.png",hsv_frame2, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            # cv2.imwrite("RGB_full.png",frame_to_bgr, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
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