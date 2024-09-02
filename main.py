import cv2
import cvzone
import time
import random
from cvzone.HandTrackingModule import HandDetector


# Open Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Track 1 hand
detector = HandDetector(maxHands = 1)

timer = 0
turnTimer = False
startGame = False
scores = [0, 0] # [AI, Player]
imgAI = None
turn = 0
showAIImage = False
aiImageStartTime = 0

# List of possible moves
moves = ["Rock", "Paper", "Scissors"]

# Game Loop
while True:
    imgBackground = cv2.imread("Resources/Background.png") # Background Image
    success, img = cap.read()

    # Scale down camera
    imgCamera = cv2.resize(img, (0, 0), None, 0.875, 0.875) 
    # Crop camera
    imgCamera = imgCamera[:, 80:480] 

    # Find Hands
    hands, img = detector.findHands(imgCamera)
    
    if startGame:

        # Timer
        if turnTimer is False:
            timer = time.time() - initialTime
            # Display Timer
            cv2.putText(imgBackground, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                turnTimer = True
                timer = 0
            
                # Count fingers
                if hands:
                    playermove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    # Sign Detection
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 'Rock' 
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 'Paper' 
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 'Scissors' 

                    aiMove = random.choice(moves) # Randomly select AI move
                    imgAI = cv2.imread(f'Resources/{aiMove}.png', cv2.IMREAD_UNCHANGED)

                    # Check if image was loaded correctly
                    if imgAI is not None: 
                        showAIImage = True
                        aiImageStartTime = time.time() # Record start time of display
                    else:
                        print(f"Error: Image Resources/{aiMove}.png could not be loaded")

                    # Play Wins
                    if (playerMove == 'Rock' and aiMove == 'Scissors') or \
                        (playerMove == 'Paper' and aiMove == 'Rock') or \
                        (playerMove == 'Scissors' and aiMove == 'Paper'):
                        scores[1] += 1

                    # AI Wins
                    if (playerMove == 'Scissors' and aiMove == 'Rock') or \
                        (playerMove == 'Rock' and aiMove == 'Paper') or \
                        (playerMove == 'Paper' and aiMove == 'Scissors'):
                        scores[0] += 1

                    turn += 1

        # Display the AI image for a specific time
        if showAIImage:
            currentTime = time.time()
            if currentTime - aiImageStartTime < 2:  # Display the AI image for 3 seconds
                imgBackground = cvzone.overlayPNG(imgBackground, imgAI, (149, 310))
            else:
                imgAI = None  # Stop displaying the AI image after 3 seconds
                showAIImage = False  # Reset the flag
                turnTimer = False  # Reset turn timer for the next round
                initialTime = time.time()  # Reset timer for the next round

                # Check if the game should end
                if turn >= 3:
                    startGame = False  # End the game after 3 rounds
                    # Determine the winner
                    if scores[1] > scores[0]:
                        winner = "Player Wins!"
                    elif scores[0] > scores[1]:
                        winner = "AI Wins!"
                    else:
                        winner = "It's a Draw!"

                    # Display the winner on the background image
                    cv2.putText(imgBackground, winner, (450, 450), cv2.FONT_HERSHEY_PLAIN, 6, (0, 255, 0), 4)
                    cv2.imshow("Background", imgBackground)
                    cv2.waitKey(3000)  # Show result for 3 seconds before exiting
                    break  # Exit the game loop
                    
    # Put camera in player block
    imgBackground[234:654, 795:1195] = imgCamera

    if turnTimer and showAIImage and imgAI is not None:
        imgBackground = cvzone.overlayPNG(imgBackground, imgAI, (149, 310))  

    # Display Scores
    cv2.putText(imgBackground, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBackground, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("Background", imgBackground)
    
    # Start the game on 's' button
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        turnTimer = False
        turn = 0 # Reset for next game
        scores = [0, 0] # Resent for next game
        showAIImage = False # Reset for next round