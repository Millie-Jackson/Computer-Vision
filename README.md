

[RPS Demo.webm](https://github.com/user-attachments/assets/3fc95eeb-60af-4d99-9746-b23791eb55da)


This project is a computer vision-based Rock-Paper-Scissors game developed using Python and OpenCV. The game detects hand gestures in real-time and allows you to play against an AI opponent. Originally, the project used a classification system built with Teachable Machine, but it has since evolved into a more flexible and robust solution using hand tracking, making it adaptable to any player and background.

Features
Advanced Computer Vision Techniques
Hand Gesture Recognition: Utilizes OpenCV and the cvzone library to track hand movements and detect gestures. This approach is robust across different users and backgrounds, and it does not require a perfectly formed hand gesture for recognition.

AI Opponent: The AI randomly selects its move (rock, paper, or scissors) to compete against the player.

Three Rounds: The game automatically advances through three rounds, after which the winner is determined and displayed on the screen.

Full-Screen Display: The game window is optimized to fit the entire screen, providing an immersive user experience.

Transition from Teachable Machine to Hand Tracking
Initially, this project used a gesture classification model trained using Google's Teachable Machine. However, to enhance flexibility and adaptability, the project was re-engineered to use a hand-tracking system. This new approach leverages OpenCV's computer vision capabilities, allowing for:

Universal Accessibility: The system works effectively with any person, regardless of skin tone or background environment.
Improved Gesture Recognition: The game does not rely on perfect hand gestures, making it more user-friendly and accurate across varying conditions.

![RPS Hand Tracking Code](Computer-Vision/Demo/RPS%20Hand%20Tracking.png?raw=true)
![RPS Hand Tracking Code](Computer-Vision/Demo/RPS%20Hand%20Tracking.png)
![RPS Hand Tracking Code](/Computer-Vision/Demo/RPS%20Hand%20Tracking.png?raw=true "Optional Title")

Requirements
Python 3.x
OpenCV (cv2)
cvzone library
A webcam
Installation
Clone the repository:
```
bash
Copy code
git clone https://github.com/Millie-Jackson/Computer-Vision.git
cd Computer-Vision
```
Install dependencies:
```
bash
Copy code
pip install opencv-python cvzone
```
Add resources:

Ensure that the required images (rock.png, paper.png, scissors.png, and Background.png) are placed in a Resources folder within the project directory.
How to Play
Start the Game:

Run the Python script:
```
bash
Copy code
python main.py
```
Press the s key to start the game.
Playing:

The game tracks your hand using the webcam and detects your gesture (rock, paper, or scissors).
After you make your move, the AI will display its move for 3 seconds.
The game proceeds automatically through three rounds.
Winning:

After three rounds, the game will display the winner on the screen.
The window will close automatically after showing the results.
Acknowledgments
The project leverages the cvzone library, which simplifies the implementation of hand tracking and other computer vision features using OpenCV.
License
This project is licensed under the MIT License.
