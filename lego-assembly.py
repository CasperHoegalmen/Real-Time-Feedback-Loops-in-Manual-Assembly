import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

cap = cv2.VideoCapture(0)
hue = 0
B = 0
G = 0
R = 0

def cameraFrame():
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Calling the individual functions.
    
        RGB2HSI(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
def RGB2HSI(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #cv2.imshow('hsv', hsv)

    #Iterate over each pixel in the image
    for x in range(0, frame.shape[1]):
        for y in range(0, frame.shape[0]):
            #Split the B, G, R channels (it is BGR and not RGB because read() function in openCV returns it in that format)
            B = frame[y, x, 0]
            G = frame[y, x, 1]
            R = frame[y, x, 2]

            #print("B is ", B)
            print("B is ", B, "\nG is ", G, "\nR is ", R)

            #Calculating Saturation
            minimum_value = min(B, min(G, R))
            saturation = 1 - 3 * (minimum_value) / (R + G + B)

            #Calculating intensity
            intensity = (B + G + R) / 3

            #Calculating Hue 
            if saturation != 0:
                hueCalculation = 0.5 * ((R - G) + (R - B)) / math.sqrt(math.pow((R - G), 2) + (R - B) * (G - B))

                # if H < -1:
                #     H = -1
                # elif H > 1:
                #     H = 1

                def hueRange(hueCalculation):
                    return min(1, max(hueCalculation, -1))
                H = hueRange(hueCalculation)

                if B <= G:        
                    hue = math.acos(H)
                elif B > G:
                    hue = 2 * math.pi - math.acos(H)

            #This is to ensure that we do not divide by 0 when calculating saturation
            if R + G + B == 0:
                saturation = 0
                intensity = 0
                hue = 0

            print("Hue is ", hue, "\nSaturation is ", saturation, "\nIntensity is ", intensity)

            frame[y, x, 0] = hue * 255 / (2 * math.pi)
            frame[y, x, 1] = saturation * 255
            frame[y, x, 2] = intensity

cameraFrame()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()