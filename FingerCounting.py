# Computer-Vision/FingerCounting.py

import cv2
import time
import os
import HandTrackingModule as htm



# Start video capture
cap = cv2.VideoCapture(0)

folderPath = "Resources/FingerImages"
imgList = os.listdir(folderPath)

overlayList = []
# Load images
for imgPath in imgList[:10]: # Load all 10 images
    image = cv2.imread(f'{folderPath}/{imgPath}')
    if image is None:
        print(f"Error loading image: {imgPath}")
    else:
        overlayList.append(image)
        print(f'Loaded image: {imgPath}, Shape: {image.shape}')

print(f'Total overlays loaded: {len(overlayList)}')

pTime = 0
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20] # Fingertip landmarks

while True:

    # Read current frame
    success, img = cap.read()
    
    # Start hand tracking
    hands, img = detector.findHands(img)
    totalFingers = 0 # Reset each frame

    # Loop through each detected hand
    for hand in hands:
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
        
    # Make sure the total number of fingers is within range (0-10)
    totalFingers =min(totalFingers, 10)
    print(f'Total fingers: {totalFingers}')

    # Make sure overlay fits in the image dimensions
    if 0 <= totalFingers < len(overlayList):
        overlayResized = cv2.resize(overlayList[totalFingers], (200, 200))
        print(f'Displaying image for {totalFingers} fingers.')

        # Ensure image fits in the camera feed dimentions
        if overlayResized.shape[0] <= img.shape[0] and overlayResized.shape[1] <= img.shape[1]:
            img[0:200, 0:200] = overlayResized
        else:
            print("Image size exceeds camera dimensions!")
    else:
        print("Invalid finger count: {totalFingers}, no image available.")

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()