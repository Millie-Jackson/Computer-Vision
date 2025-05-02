import cv2
import time
import random
import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.HandTrackingModule import handDetector
from scripts.data_analysis import analyze_player_patterns, get_smart_ai_move, save_moves_to_csv, display_moves_as_dataframe, check_dataset_size, calculate_ai_win_rate



logging.basicConfig(
    filename='logs/rock_paper_scissors.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    level=logging.INFO
)

# Open Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Track 1 hand
detector = handDetector(maxHands = 1)

# Game variables
timer = 0
turnTimer = False
startGame = False
scores = [0, 0] # [AI, Player]
imgAI = None
turn = 0
showAIImage = False
aiImageStartTime = 0
player_move_history = []
ai_move_history = []
round_results = [] # 'AI Wins', 'Player Wins', 'Draw'

# List of possible moves
moves = ["Rock", "Paper", "Scissors"]

# Create a fullscreen window
cv2.namedWindow("Background", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Background", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)



def overlayPNG(background, img, pos=(0, 0)) -> list:

    # Ensure image sizes match
    y_offset, x_offset = pos
    y1, y2 = y_offset, y_offset + img.shape[0]
    x1, x2 = x_offset, x_offset + img.shape[1]

    alpha_img = img[:, :, 3] / 255.0 # Alpha channel
    alpha_background = 1.0 - alpha_img

    for c in range(0, 3):
        background[y1:y2, x1:x2, c] = (alpha_img * img[:, :, c] + alpha_background * background[y1:y2, x1:x2, c])

    return background


try:
    # Game Loop
    logging.info('Game started')
    while True:
        imgBackground = cv2.imread("resources/background.png") # Background Image
        
        if imgBackground is None:
            logging.error("Background image not found or failed to load.")
            break
        
        success, img = cap.read()

        if not success or img is None:
            logging.warning("Webcam frame not captured.")
            continue

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
                    logging.info(f'Round {turn + 1} started')
                    turnTimer = True
                    timer = 0
                
                    # Count fingers
                    if hands:
                        playerMove = None
                        hand = hands[0]
                        fingers = detector.fingersUp(hand)
                        # Sign Detection
                        if fingers == [0, 0, 0, 0, 0]:
                            playerMove = 'Rock' 
                        if fingers == [1, 1, 1, 1, 1]:
                            playerMove = 'Paper' 
                        if fingers == [0, 1, 1, 0, 0]:
                            playerMove = 'Scissors' 

                        player_move_history.append(playerMove)
                        aiMove = get_smart_ai_move(player_move_history) or random.choice(moves)
                        ai_move_history.append(aiMove)
                        logging.debug(f'Player move: {playerMove}')
                        logging.debug(f'Predicted: {aiMove}, AI move: {aiMove}')
                        
                        imgAI = cv2.imread(f'resources/{aiMove}.png', cv2.IMREAD_UNCHANGED)

                        # Check if image was loaded correctly
                        if imgAI is not None: 
                            showAIImage = True
                            aiImageStartTime = time.time() # Record start time of display
                        else:
                            logging.warning(f'Image not found: resources/{aiMove}.png')

                        # Play Wins
                        if (playerMove == 'Rock' and aiMove == 'Scissors') or \
                            (playerMove == 'Paper' and aiMove == 'Rock') or \
                            (playerMove == 'Scissors' and aiMove == 'Paper'):
                            scores[1] += 1
                            round_results.append("Player Wins")

                        # AI Wins
                        if (playerMove == 'Scissors' and aiMove == 'Rock') or \
                            (playerMove == 'Rock' and aiMove == 'Paper') or \
                            (playerMove == 'Paper' and aiMove == 'Scissors'):
                            scores[0] += 1
                            round_results.append("AI Wins")
                        
                        # Record a Draw
                        if playerMove == aiMove:
                            round_results.append("Draw")

                        logging.info(f'Round {turn + 1} result: {round_results[-1]}')
                        turn += 1



            # Display the AI image for a specific time
            if showAIImage:
                currentTime = time.time()
                if currentTime - aiImageStartTime < 2:  # Display the AI image for 3 seconds
                    imgBackground = overlayPNG(imgBackground, imgAI, (300, 150))
                else:
                    imgAI = None  # Stop displaying the AI image after 3 seconds
                    showAIImage = False  # Reset the flag
                    turnTimer = False  # Reset turn timer for the next round
                    initialTime = time.time()  # Reset timer for the next round

                    # Check if the game should end
                    if turn >= 3:
                        logging.info(analyze_player_patterns(player_move_history))
                        logging.info(f'Game Over: Player {scores[1]} - AI {scores[0]}')
                        startGame = False  # End the game after 3 rounds
                        # Determine the winner
                        if scores[1] > scores[0]:
                            # cv2 doesnt support \n so each on a line of its own
                            cv2.putText(imgBackground, "Player", (807, 420), cv2.FONT_HERSHEY_PLAIN, 6, (0, 255, 0), 4)
                            cv2.putText(imgBackground, "Wins!", (845, 485), cv2.FONT_HERSHEY_PLAIN, 6, (0, 255, 0), 4)
                        elif scores[0] > scores[1]:
                            # cv2 doesnt support \n so each on a line of its own
                            cv2.putText(imgBackground, "AI", (207, 420), cv2.FONT_HERSHEY_PLAIN, 6, (0, 255, 0), 4)
                            cv2.putText(imgBackground, "Wins!", (145, 485), cv2.FONT_HERSHEY_PLAIN, 6, (0, 255, 0), 4)
                        else:
                            winner = "It's a Draw!"
                            cv2.putText(imgBackground, winner, (400, 450), cv2.FONT_HERSHEY_PLAIN, 6, (0, 255, 0), 4)

                        cv2.imshow("Background", imgBackground)
                        cv2.waitKey(3000)  # Show result for 3 seconds before exiting
                        break  # Exit the game loop
                        
        # Put camera in player block
        if imgCamera is not None:
            imgBackground[234:654, 795:1195] = imgCamera 
        else: 
            logging.warning("imgCamera is None - skipping frame assignment.")

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
        
        elif key == 27: # ESC
            logging.info("Escape key pressed. Exiting Game.")
            break

except Exception as e:
    logging.exception("Unexpected error occurred during game loop.")

finally:
    logging.info(f'Saving game data to CSV with {len(player_move_history)} rounds')
    cap.release()
    cv2.destroyAllWindows

# Save moves to dataset
df = display_moves_as_dataframe(player_move_history, ai_move_history)
save_moves_to_csv(player_move_history, ai_move_history, round_results)
check_dataset_size()
calculate_ai_win_rate(round_results)



# End of File