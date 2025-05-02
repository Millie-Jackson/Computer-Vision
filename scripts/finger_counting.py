# Computer-Vision/FingerCounting.py

import cv2
import time
import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import modules.HandTrackingModule as htm



logging.basicConfig(
    filename='logs/finger_counting.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    level=logging.INFO
)

# Start video capture
logging.info("Initializing video capture...")
cap = cv2.VideoCapture(0)

folderPath = "resources/FingerImages"
imgList = os.listdir(folderPath)

overlayList = []
# Load images
logging.info("Loading overlay images from folderPath: %s", folderPath)
for imgPath in imgList[:10]: # Load all 10 images
    image = cv2.imread(f'{folderPath}/{imgPath}')
    if image is None:
        logging.info(f"Error loading image: {imgPath}")
    else:
        overlayList.append(image)
        logging.info(f'Loaded image: {imgPath}, Shape: {image.shape}')

logging.info(f'Total overlays loaded: {len(overlayList)}')

pTime = 0
logging.info("Initializing hand detector...")
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20] # Fingertip landmarks

while True:

    # Read current frame
    logging.debug("Reading frame from camera...")
    success, img = cap.read()
    if not success or img is None:
        logging.warning("Failed to read frame from webcam.")
        continue
    
    # Start hand tracking
    hands, img = detector.findHands(img)
    totalFingers = 0 # Reset each frame

    # Loop through each detected hand
    for hand in hands:
        logging.debug("Hand detected. Checking fingers...")
        # Check if there is a hand
        if len(hands) == 0:
            continue  # If no hand - skip

        # Get list of finger up
        fingers = detector.fingersUp(hand)

        if hand == hands[0]: # Left hand
            # Manually check the thumb
            if hand.landmark[tipIds[0]].x < hand.landmark[tipIds[0] - 1].x:
                fingers[0] = 1 # Thumb is up
            else:
                fingers[0] = 0 # Thumb is down
        else: # Right hand
            if hand.landmark[tipIds[0]].x > hand.landmark[tipIds[0] - 1].x:
                fingers[0] = 1 # Thumb is up
            else:
                fingers[0] = 0 # Thumb is down

        # Count fingers
        totalFingers += fingers.count(1)
        logging.info(f'Total fingers detected: {totalFingers}')
        
    # Make sure the total number of fingers is within range (0-10)
    totalFingers =min(totalFingers, 10)
    logging.info(f'Total fingers: {totalFingers}')

    # Make sure overlay fits in the image dimensions
    if 0 <= totalFingers < len(overlayList):
        overlayResized = cv2.resize(overlayList[totalFingers], (200, 200))
        logging.info(f'Displaying image for {totalFingers} fingers.')

        # Ensure image fits in the camera feed dimentions
        if overlayResized.shape[0] <= img.shape[0] and overlayResized.shape[1] <= img.shape[1]:
            img[0:200, 0:200] = overlayResized
        else:
            logging.info("Image size exceeds camera dimensions!")
    else:
        logging.info("Invalid finger count: {totalFingers}, no image available.")

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        logging.info("Quitting application. Releasing resources.")

        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()