import numpy as np
#from pyueye import ueye
#from lego_api import CameraApi
from server import Connection
import cv2
import threading

# Variables
# Threshold values for the blue brick
blue_low_hue = 105
blue_high_hue = 126

blue_low_sat = 204
blue_high_sat = 255

blue_low_val = 90
blue_high_val = 255

# Threshold values for the green brick
green_low_hue = 51
green_high_hue = 88

green_low_sat = 81
green_high_sat = 255

green_low_val = 0
green_high_val = 255

# Threshold values for the red brick
red_low_hue = 173
red_high_hue = 179

red_low_sat = 177
red_high_sat = 255

red_low_val = 66
red_high_val = 255

# Morphology Kernel
general_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))

assembly_step_number = ""
integer_step_number = 0
current_brick_color = ""
current_shape = False

second_layer_shape = False

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
    global current_shape

    global second_layer_shape

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

    #Apply morphology to the created masks
    blue_mask_morph = frame_morph(general_kernel, frame, blue_mask, cv2.MORPH_CLOSE)
    green_mask_morph = frame_morph(general_kernel, frame, green_mask, cv2.MORPH_CLOSE)
    red_mask_morph = frame_morph(general_kernel, frame, red_mask, cv2.MORPH_CLOSE)

    n_white_red_color = np.sum(red_mask_morph == 255)
    n_white_green_color = np.sum(green_mask_morph == 255)  
    n_white_blue_color = np.sum(blue_mask_morph == 255)

    # print("red color = ", n_white_red_color)
    # print("green color = ", n_white_green_color)
    # print("blue color = ", n_white_blue_color)

    #Color identification that is used in the error feedback function
    color_function(n_white_red_color, n_white_green_color, n_white_blue_color)

    #Composite mask
    blue_red_mask = blue_mask_morph + red_mask_morph
    final_mask = blue_red_mask + green_mask_morph
    comp_result = cv2.bitwise_and(frame, frame, mask = final_mask)

    # Perform Blob Analysis
    #2x4 bricks
    blue_blobs_2x4 = blob_analysis(blue_mask_morph, 3300, 3600, 'blue', '2x4')
    green_blobs_2x4 = blob_analysis(green_mask_morph, 3300, 3600, 'green', '2x4')
    red_blobs_2x4 = blob_analysis(red_mask_morph, 3300, 3600, 'red', '2x4')

    #2x2 bricks
    blue_blobs_2x2 = blob_analysis(blue_mask_morph, 3700, 3900, 'blue', '2x2')
    green_blobs_2x2 = blob_analysis(green_mask_morph, 3700, 3900, 'green', '2x2')
    red_blobs_2x2 = blob_analysis(red_mask_morph, 3700, 3900, 'red', '2x2')

    #Error detection feedback
    assembly_step_number = Connection.string_message
    sum_of_correct_shapes = len(blue_blobs_2x4) + len(green_blobs_2x4) + len(red_blobs_2x4)
    if sum_of_correct_shapes > 0 and sum_of_correct_shapes <= 5:
        current_shape = True

    second_layer_sum_of_shapes = len(blue_blobs_2x2) + len(green_blobs_2x2) + len(red_blobs_2x2)
    if second_layer_sum_of_shapes > 0 and second_layer_sum_of_shapes <= 3:
        current_shape = False
        second_layer_shape = True

    error_feedback(assembly_step_number, current_brick_color, current_shape, second_layer_shape)

    current_shape = False
    second_layer_shape = False

    # Result of all 'rings' that are to be drawn around each of the BLOBs
    final_number_of_blobs = blue_blobs_2x4 + green_blobs_2x4 + red_blobs_2x4

    second_layer_number_of_blobs = blue_blobs_2x2 + green_blobs_2x2 + red_blobs_2x2
 
    #Show... Change the second argument to the blue/green/redResultMorph variables to show the result with morphology
    cv2.imshow('Blue Color Mask old', blue_mask_morph)
    cv2.imshow('Green Color Mask', green_mask_morph)
    cv2.imshow('Red Color Mask', red_mask_morph)
    
    #n_white_pix = np.sum(green_mask_morph == 255)
    #print(n_white_pix)
            
    frame_with_keypoints = cv2.drawKeypoints(comp_result, final_number_of_blobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    second_layer_frame_with_keypoints = cv2.drawKeypoints(comp_result, second_layer_number_of_blobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow('Composite Frame', frame_with_keypoints)

def frame_morph(kernel, frame_original, frame_to_be_morphed, morphology_method):
    mask_morph = cv2.morphologyEx(frame_to_be_morphed, morphology_method, kernel)
    return mask_morph

def color_function(red, green, blue):
    global current_brick_color

    #if np.array(red).any() != 0:
    if red > 500:
        current_brick_color = "Red"

    #elif np.array(green).any() != 0:
    elif green > 500:
        current_brick_color = "Green"

    #elif np.array(blue).any() != 0:
    elif blue > 500:
        current_brick_color = "Blue"

    else: 
        current_brick_color = "No predefined color is detected"

    return current_brick_color

def blob_analysis(frame, min_area, max_area, color, brick_type):
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
    #     print('Number of ' + str(color) + ' ' + str(brick_type) + ' Bricks: ' + str(len(keypoints)))

    #print(len(keypoints))

    return keypoints

def error_feedback(step_number, color_to_use, shape_to_use, second_layer_shape_to_use):
    global integer_step_number

    if step_number != "":
        integer_step_number = int(step_number)

    print("Step number is ", integer_step_number)
    #print("Color is " + color_to_use)
    #print("Shape is ", shape_to_use)

    if integer_step_number == 1:
        if shape_to_use == True:
            Connection.shape_feedback = "Correct"
        else:
            Connection.shape_feedback = "Incorrect"

        if color_to_use == "Red":
            Connection.color_feedback = "Correct"
        else:
            Connection.color_feedback = "Incorrect"
    
    elif integer_step_number == 2:
        if shape_to_use == True:
            Connection.shape_feedback = "Correct"
        else:
            Connection.shape_feedback = "Incorrect"

        if color_to_use == "Blue":
            Connection.color_feedback = "Correct"
        else:
            Connection.color_feedback = "Incorrect"

    elif integer_step_number == 3:
        if shape_to_use == True:
            Connection.shape_feedback = "Correct"
        else:
            Connection.shape_feedback = "Incorrect"

        if color_to_use == "Red":
            Connection.color_feedback = "Correct"
        else:
            Connection.color_feedback = "Incorrect"

    elif integer_step_number == 4:
        if shape_to_use == True:
            Connection.shape_feedback = "Correct"
        else:
            Connection.shape_feedback = "Incorrect"

        if color_to_use == "Green":
            Connection.color_feedback = "Correct"
        else:
            Connection.color_feedback = "Incorrect"

    elif integer_step_number == 5:
        if shape_to_use == True:
            Connection.shape_feedback = "Correct"
        else:
            Connection.shape_feedback = "Incorrect"

        if color_to_use == "Blue":
            Connection.color_feedback = "Correct"
        else:
            Connection.color_feedback = "Incorrect"

    elif integer_step_number == 6:
        if second_layer_shape_to_use == True:
            Connection.shape_feedback = "Correct"
        else:
            Connection.shape_feedback = "Incorrect"

        if color_to_use == "Blue":
            Connection.color_feedback = "Correct"
        else:
            Connection.color_feedback = "Incorrect"

    elif integer_step_number == 7:
        if second_layer_shape_to_use == True:
            Connection.shape_feedback = "Correct"
        else:
            Connection.shape_feedback = "Incorrect"

        if color_to_use == "Green":
            Connection.color_feedback = "Correct"
        else:
            Connection.color_feedback = "Incorrect"

    elif integer_step_number == 8:
        if second_layer_shape_to_use == True:
            Connection.shape_feedback = "Correct"
        else:
            Connection.shape_feedback = "Incorrect"

        if color_to_use == "Red":
            Connection.color_feedback = "Correct"
        else:
            Connection.color_feedback = "Incorrect"

    else: 
        Connection.shape_feedback = "Incorrect"
        Connection.color_feedback = "Incorrect"
        

#Temporary
cap = cv2.VideoCapture(0)

def main_loop():

    color_trackbars()

    while(cap.isOpened()):

        # In order to display the image in an OpenCV window we need to...
        # ...extract the data of our image memory
        #array = ueye.get_data(CameraApi.pcImageMemory, CameraApi.width, CameraApi.height, CameraApi.nBitsPerPixel, CameraApi.pitch, copy=False)

        # bytes_per_pixel = int(nBitsPerPixel / 8)

        # ...reshape it in an numpy array...
        #frame = np.reshape(array,(CameraApi.height.value, CameraApi.width.value, CameraApi.bytes_per_pixel))

        # ...resize the image by a half
        #frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
        
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
    #---------------------------------------------------------------------------------------------------------------------------------------
        #Include image data processing here
        #frame_to_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)


        #step = Connection.string_message

        #Convert camera feed from BGR color space to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #Apply a Gaussian blur that has 11x11 kernel size to the camera frame 
        frame = cv2.GaussianBlur(frame, (11, 11), 0)

        frame_threshold(frame, hsv_frame)
    #---------------------------------------------------------------------------------------------------------------------------------------

        #...and finally display it
        cv2.imshow("HSV frame", hsv_frame)

        #print(Connection.string_message)

        # Press q if you want to end the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #---------------------------------------------------------------------------------------------------------------------------------------

    # Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
    #ueye.is_FreeImageMem(CameraApi.hCam, CameraApi.pcImageMemory, CameraApi.MemID)

    # Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
    #ueye.is_ExitCamera(CameraApi.hCam)

    # Destroys the OpenCv windows
    cv2.destroyAllWindows()

    print()
    print("END")

if __name__ == "__main__":
    t1 = threading.Thread(target = Connection.server)
    t2 = threading.Thread(target = main_loop)

    t1.start()
    t2.start()

#CameraApi.initialize_camera()