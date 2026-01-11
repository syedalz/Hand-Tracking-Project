"""
Hand Tracking Module using OpenCV and MediaPipe

This program detects hands from a webcam feed, draws hand landmarks,
and extracts pixel coordinates of each hand landmark in real time.

Author: AliZ
Purpose: Learning computer vision and hand tracking fundamentals
"""


import cv2
import mediapipe as mp
import time


# HandDetector class encapsulates all hand tracking logic
class HandDetector():

    # Constructor: runs when an object of HandDetector is created
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # Whether to treat input as static images (False for video)
        self.mode = mode

        # Maximum number of hands to detect
        self.maxHands = maxHands

        # Minimum confidence required to detect a hand
        self.detectionCon = detectionCon

        # Minimum confidence required to track hand landmarks
        self.trackCon = trackCon

        # Load MediaPipe Hands solution
        self.mpHands = mp.solutions.hands

        # Create a Hands object with the specified parameters
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        # Utility used to draw hand landmarks on images
        self.mpDraw = mp.solutions.drawing_utils


    # Detect hands and optionally draw landmarks
    def findHands(self, img, draw=True):

        # Convert image from BGR (OpenCV default) to RGB (MediaPipe requirement)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the image and detect hands
        self.results = self.hands.process(imgRGB)

        # If hands are detected, draw landmarks
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw points and connections on the hand
                    self.mpDraw.draw_landmarks(
                        img,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS
                    )

        # Return the image
        return img


    # Get positions (x, y) of all landmarks for one hand
    def findPosition(self, img, handNo=0, draw=True):

        lmList = []  # List to store landmark positions

        # Check if any hands were detected
        if self.results.multi_hand_landmarks:

            # Select one hand (default: first hand)
            myHand = self.results.multi_hand_landmarks[handNo]

            # Loop through all 21 landmarks
            for id, lm in enumerate(myHand.landmark):

                # Get image dimensions
                height, width, channel = img.shape

                # Convert normalized coordinates (0–1) to pixel values
                cx, cy = int(lm.x * width), int(lm.y * height)

                # Store landmark id and coordinates
                lmList.append([id, cx, cy])

                # Draw a small circle at each landmark
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        # Return the list of landmarks
        return lmList


# Main function
def main():

    prevTime = 0  # Previous frame time
    currTime = 0  # Current frame time

    # Open webcam (0 = default camera)
    cap = cv2.VideoCapture(0)

    # Create HandDetector object
    detector = HandDetector()

    # Infinite loop to read webcam frames
    while True:

        # Read frame from webcam
        success, img = cap.read()

        # Detect hands and draw landmarks
        img = detector.findHands(img)

        # Get landmark positions
        lmList = detector.findPosition(img)


        # Calculate FPS
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        # Display FPS on the screen
        cv2.putText(
            img,
            str(int(fps)),
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            3,
            (0, 0, 255),
            3
        )

        # Show the video feed
        cv2.imshow("Hand Tracking", img)

        # Wait 1ms (required for OpenCV window to update)
        cv2.waitKey(1)


# Run the program
if __name__ == "__main__":
    main()
