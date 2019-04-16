import numpy as np
from pyueye import ueye
import cv2
import sys

class CameraApi:
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
    nRet = ""
    width = rectAOI.s32Width
    height = rectAOI.s32Height

    @staticmethod
    def initialize_camera():
            
        #---------------------------------------------------------------------------------------------------------------------------------------
        print("START")
        print()

        # Starts the driver and establishes the connection to the camera
        CameraApi.nRet = ueye.is_InitCamera(CameraApi.hCam, None)
        if CameraApi.nRet != ueye.IS_SUCCESS:
            print("is_InitCamera ERROR")

        # Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
        CameraApi.nRet = ueye.is_GetCameraInfo(CameraApi.hCam, CameraApi.cInfo)
        if CameraApi.nRet != ueye.IS_SUCCESS:
            print("is_GetCameraInfo ERROR")

        # You can query additional information about the sensor type used in the camera
        CameraApi.nRet = ueye.is_GetSensorInfo(CameraApi.hCam, CameraApi.sInfo)
        if CameraApi.nRet != ueye.IS_SUCCESS:
            print("is_GetSensorInfo ERROR")

        CameraApi.nRet = ueye.is_ResetToDefault(CameraApi.hCam)
        if CameraApi.nRet != ueye.IS_SUCCESS:
            print("is_ResetToDefault ERROR")

        # Set display mode to DIB
        CameraApi.nRet = ueye.is_SetDisplayMode(CameraApi.hCam, ueye.IS_SET_DM_DIB)

        # Set the right color mode
        if int.from_bytes(CameraApi.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
            # setup the color depth to the current windows setting
            ueye.is_GetColorDepth(CameraApi.hCam, CameraApi.nBitsPerPixel, CameraApi.m_nColorMode)
            CameraApi.bytes_per_pixel = int(CameraApi.nBitsPerPixel / 8)
            print("IS_COLORMODE_BAYER: ", )
            print("\tm_nColorMode: \t\t", CameraApi.m_nColorMode)
            print("\tnBitsPerPixel: \t\t", CameraApi.nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", CameraApi.bytes_per_pixel)
            print()

        elif int.from_bytes(CameraApi.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
            # for color camera models use RGB32 mode
            m_nColorMode = ueye.IS_CM_BGRA8_PACKED
            nBitsPerPixel = ueye.INT(32)
            CameraApi.bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_CBYCRY: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", CameraApi.bytes_per_pixel)
            print()

        elif int.from_bytes(CameraApi.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
            # for color camera models use RGB32 mode
            m_nColorMode = ueye.IS_CM_MONO8
            nBitsPerPixel = ueye.INT(8)
            CameraApi.bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_MONOCHROME: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", CameraApi.bytes_per_pixel)
            print()

        else:
            # for monochrome camera models use Y8 mode
            m_nColorMode = ueye.IS_CM_MONO8
            nBitsPerPixel = ueye.INT(8)
            CameraApi.bytes_per_pixel = int(nBitsPerPixel / 8)
            print("else")

        # Can be used to set the size and position of an "area of interest"(AOI) within an image
        CameraApi.nRet = ueye.is_AOI(CameraApi.hCam, ueye.IS_AOI_IMAGE_GET_AOI, CameraApi.rectAOI, ueye.sizeof(CameraApi.rectAOI))
        if CameraApi.nRet != ueye.IS_SUCCESS:
            print("is_AOI ERROR")

        CameraApi.width = CameraApi.rectAOI.s32Width
        CameraApi.height = CameraApi.rectAOI.s32Height


        # Prints out some information about the camera and the sensor
        print("Camera model:\t\t", CameraApi.sInfo.strSensorName.decode('utf-8'))
        print("Camera serial no.:\t", CameraApi.cInfo.SerNo.decode('utf-8'))
        print("Maximum image width:\t", CameraApi.width)
        print("Maximum image height:\t", CameraApi.height)
        print()

        #---------------------------------------------------------------------------------------------------------------------------------------

        # Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
        CameraApi.nRet = ueye.is_AllocImageMem(CameraApi.hCam, CameraApi.width, CameraApi.height, CameraApi.nBitsPerPixel, CameraApi.pcImageMemory, CameraApi.MemID)
        if CameraApi.nRet != ueye.IS_SUCCESS:
            print("is_AllocImageMem ERROR")
        else:
            # Makes the specified image memory the active memory
            CameraApi.nRet = ueye.is_SetImageMem(CameraApi.hCam, CameraApi.pcImageMemory, CameraApi.MemID)
            if CameraApi.nRet != ueye.IS_SUCCESS:
                print("is_SetImageMem ERROR")
            else:
                # Set the desired color mode
                CameraApi.nRet = ueye.is_SetColorMode(CameraApi.hCam, CameraApi.m_nColorMode)

        # Activates the camera's live video mode (free run mode)
        CameraApi.nRet = ueye.is_CaptureVideo(CameraApi.hCam, ueye.IS_DONT_WAIT)
        if CameraApi.nRet != ueye.IS_SUCCESS:
            print("is_CaptureVideo ERROR")

        # Enables the queue mode for existing image memory sequences
        CameraApi.nRet = ueye.is_InquireImageMem(CameraApi.hCam, CameraApi.pcImageMemory, CameraApi.MemID, CameraApi.width, CameraApi.height, CameraApi.nBitsPerPixel, CameraApi.pitch)
        if CameraApi.nRet != ueye.IS_SUCCESS:
            print("is_InquireImageMem ERROR")
        else:
            print("Press q to leave the programm")        