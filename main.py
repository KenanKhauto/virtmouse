import cv2
import mediapipe as mp
import pyautogui

from rules import is_index_finger_up, are_index_and_middle_fingers_up
from utils import distance, kalman_filter, clamp

# Get screen size
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
previous_y = None

def main():
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    while True:
        success, img = cap.read()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if is_index_finger_up(mp_hands, hand_landmarks):
                    
                    # Get coordinates of the index finger
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    smoothed_x, smoothed_y = kalman_filter(index_finger_tip.x, index_finger_tip.y)
                    smoothed_x = clamp(smoothed_x, 1, SCREEN_WIDTH - 1)
                    smoothed_y = clamp(smoothed_y, 1, SCREEN_HEIGHT - 1)
                    pyautogui.moveTo(index_finger_tip.x * SCREEN_WIDTH, index_finger_tip.y * SCREEN_HEIGHT)
                
                if are_index_and_middle_fingers_up(mp_hands, hand_landmarks):
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    # Calculate the midpoint of the index and middle finger tips
                    current_y = (index_finger_tip.y + middle_finger_tip.y) / 2
                    if previous_y is not None:
                        # Compare the previous and current y-positions to determine the scroll direction
                        if current_y > previous_y:
                            # Hand is moving down, scroll down
                            pyautogui.scroll(-300)
                        elif current_y < previous_y:
                            # Hand is moving up, scroll up
                            pyautogui.scroll(300)

                    # Update the previous y-position for the next loop
                    previous_y = current_y
                else:
                    # Reset previous_y when gesture is not detected
                    previous_y = None

    
                # thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                # dist = distance(thumb_tip, index_finger_tip)

                # if dist < 0.05:  # Adjust threshold based on testing
                #     pyautogui.click()

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()