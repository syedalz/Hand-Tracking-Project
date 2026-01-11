import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        # Convert BGR image (OpenCV) to RGB (MediaPipe requirement)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process image and detect hands
        self.results = self.hands.process(imgRGB)

        # prints the raw hand landmark data
        #print(results.multi_hand_landmarks)

        # draw hand and landmark connections
        if (self.results.multi_hand_landmarks):
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img


    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if (self.results.multi_hand_landmarks):
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                height, width, channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)


        return lmList


def main():

    prevTime = 0
    currTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        # show fps
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)

        # Show image
        cv2.imshow("Hand Tracking", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()