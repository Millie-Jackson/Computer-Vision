import cv2
import mediapipe as mp
import time

class handDetector():
    """
    A class for detecting hands using the Mediapipe Hands solution.
    
    Attributes:
    -----------
    mode : bool
        Static mode for the hand detection. If False, it will detect and track hands continuously.
    maxHands : int
        Maximum number of hands to detect.
    detectionCon : float
        Minimum confidence for detecting hands.
    trackCon : float
        Minimum confidence for tracking hands.
    results : object
        Stores the result of the hand detection.
    mpHands : object
        Mediapipe hands solution.
    hands : object
        Initialized Mediapipe hands object with the given parameters.
    mpDraw : object
        Mediapipe drawing utility for drawing hand landmarks and connections.
    """

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        """
        Initializes the hand detector object with the given parameters.

        Parameters:
        -----------
        mode : bool, optional
            Static mode for the hand detection (default is False).
        maxHands : int, optional
            Maximum number of hands to detect (default is 2).
        detectionCon : float, optional
            Minimum confidence for detecting hands (default is 0.5).
        trackCon : float, optional
            Minimum confidence for tracking hands (default is 0.5).
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.results = None

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 
                                        min_detection_confidence=self.detectionCon, 
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        """
        Processes an image to detect hands and optionally draws the hand landmarks.

        Parameters:
        -----------
        img : numpy array
            The input image in BGR format.
        draw : bool, optional
            If True, draws the detected hand landmarks on the image (default is True).

        Returns:
        --------
        img : numpy array
            The processed image with hand landmarks drawn if draw is True.
        """

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
        self.results = self.hands.process(imgRGB)
        hands = []

        # Check for multiple hands
        if self.results.multi_hand_landmarks:
            hands = self.results.multi_hand_landmarks # Store the landmarks

            for handsLms in self.results.multi_hand_landmarks:
                # Only draw if we ask it too
                if draw:
                    # Draw the 21 landmarks and connections
                    self.mpDraw.draw_landmarks(img, handsLms, self.mpHands.HAND_CONNECTIONS)

        return hands, img # Incase we drew on it
    
    def findPosition(self, img, handNumber=0, draw=True):
        """
        Finds the positions of hand landmarks and optionally draws them on the image.

        Parameters:
        -----------
        img : numpy array
            The input image in BGR format.
        handNumber : int, optional
            The index of the hand to extract landmarks from (default is 0).
        draw : bool, optional
            If True, draws the landmarks' positions as circles on the image (default is True).

        Returns:
        --------
        lmList : list
            A list of [id, cx, cy] for each landmark where:
            id = landmark index,
            cx = x-coordinate of the landmark,
            cy = y-coordinate of the landmark.
        """
        
        lmList = [] # List of all landmark positions

        if self.results.multi_hand_landmarks:
            handsLms = self.results.multi_hand_landmarks[handNumber]
            # Extract each hand
            for id, lm in enumerate(handsLms.landmark): # lm = landmark | id = which landmark
                #print(id, lm)
                h, w, c = img.shape # width, height, channel
                cx, cy = int(lm.x * w), int(lm.y * h) # position of center
                print(id, cx, cy)
                lmList.append([id, cx, cy])
                
                # Draw by default
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
    
        return lmList # Even if it is 0
    
    def fingersUp(self, hand) -> list:
        """
        Determines which fingers are up based on the landmarks of the hand.

        Parameters:
        -----------
        hand : multi_hand_landmarks
            The hand landmarks data from Mediapipe.

        Returns:
        --------
        fingers : list
            A list of 0s and 1s, where 1 means the finger is up, and 0 means it's down.
            The order of fingers is: Thumb, Index, Middle, Ring, Pinky.
        """

        fingers = []
        # Finger tips
        tips = [4, 8, 12, 16, 20] # Thumb | Index | Middle | Ring | Pinkey

        # Thumb (compare x because it bends horizontally)
        if hand.landmark[tips[0]].x < hand.landmark[tips[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers (compare y because they bend vertically)
        for id in range(1, 5):
            if hand.landmark[tips[id]].y < hand.landmark[tips[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers



def main():
    """
    Main function to test the hand detection module.
    
    Captures video from the webcam, detects hands, and displays the video with 
    FPS and hand landmarks.
    """
        
    # FPS Tracker
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[20])

        # FPS Tracker
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    


if __name__ == "__main__":
    main()