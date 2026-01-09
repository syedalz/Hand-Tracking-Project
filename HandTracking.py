import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Utility to draw landmarks
mpDraw = mp.solutions.drawing_utils

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    # Convert BGR image (OpenCV) to RGB (MediaPipe requirement)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process image and detect hands
    results = hands.process(imgRGB)

    print(results)

    # Show image
    cv2.imshow("Hand Tracking", img)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
