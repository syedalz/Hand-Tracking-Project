"""
System Volume Control using Hand Gestures

This program uses real-time hand tracking from a webcam to control
the system's master volume by measuring the distance between the
thumb and index finger. Windows Core Audio is accessed through Pycaw
to adjust volume levels dynamically.

Author: AliZ
Purpose: Applying computer vision and OS-level audio control
"""

import cv2
import time
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#########################
# Camera resolution
camWidth, camHeight = 640, 480
##########################

# Initialize webcam (0 = default camera)
cap = cv2.VideoCapture(0)

# Set webcam width
cap.set(3, camWidth)

# Set webcam height
cap.set(4, camHeight)

# Store previous time for FPS calculation
prevTime = 0

# Create hand detector object with higher detection confidence
detector = htm.HandDetector(detectionCon=0.7)


# Get default audio output device (speakers)
devices = AudioUtilities.GetSpeakers()

# Activate audio interface
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)

# Cast interface to volume control object
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get volume range (min, max, step)
volRange = volume.GetVolumeRange()

# Extract min and max volume levels
minVol = volRange[0]
maxVol = volRange[1]

# Initialize volume-related variables
vol = 0
volBar = 400
volPer = 0


# Main loop (runs continuously)
while True:

    # Read frame from webcam
    success, img = cap.read()

    # Detect hands and draw landmarks
    img = detector.findHands(img)

    # Get landmark positions (do not draw dots)
    lmList = detector.findPosition(img, draw=False)

    # If landmarks are detected
    if len(lmList) != 0:

        # Print thumb tip (4) and index tip (8)
        print(lmList[4], lmList[8])

        # Get coordinates of thumb tip
        x1, y1 = lmList[4][1], lmList[4][2]

        # Get coordinates of index fingertip
        x2, y2 = lmList[8][1], lmList[8][2]

        # Calculate center point between fingers
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        # Draw circles on thumb and index fingertips
        cv2.circle(img, (int(x1), int(y1)), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (int(x2), int(y2)), 15, (255, 0, 0), cv2.FILLED)

        # Draw line between thumb and index finger
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        # Draw center point
        cv2.circle(img, (int(cx), int(cy)), 15, (255, 0, 0), cv2.FILLED)

        # Calculate distance between fingers
        length = math.hypot(x2 - x1, y2 - y1)

        # Hand distance range: 50 → 300
        # Volume range: minVol → maxVol

        # Map finger distance to system volume
        vol = np.interp(length, [50, 300], [minVol, maxVol])

        # Map finger distance to volume bar height
        volBar = np.interp(length, [50, 300], [400, 150])

        # Map finger distance to percentage
        volPer = np.interp(length, [50, 300], [0, 100])

        # Set system volume
        volume.SetMasterVolumeLevel(vol, None)

        # Visual feedback when fingers are very close
        if length < 50:
            cv2.circle(img, (int(cx), int(cy)), 15, (0, 255, 0), cv2.FILLED)

        # Draw volume bar outline
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)

        # Draw filled volume bar
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

        # Display volume percentage
        cv2.putText(
            img, f'{int(volPer)} %', (40, 450),
            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2
        )

        # FPS calculation
        currentTime = time.time()
        fps = 1 / (currentTime - prevTime)
        prevTime = currentTime

        # Display FPS
        cv2.putText(
            img, f'FPS: {int(fps)}', (40, 50),
            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2
        )

        # Show image
        cv2.imshow("Image", img)

        # Small delay to allow OpenCV to update window
        cv2.waitKey(1)
