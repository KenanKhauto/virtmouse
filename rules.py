
def are_index_and_middle_fingers_up(mp_hands, hand_landmarks):
    # Index Finger landmarks
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

    # Middle Finger landmarks
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    middle_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

    # Ring Finger and Pinky landmarks
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    # Condition 1: Check if the index finger is extended
    index_finger_extended = (index_finger_tip.y < index_finger_dip.y and 
                             index_finger_dip.y < index_finger_pip.y and 
                             index_finger_pip.y < index_finger_mcp.y)

    # Condition 2: Check if the middle finger is extended
    middle_finger_extended = (middle_finger_tip.y < middle_finger_dip.y and 
                              middle_finger_dip.y < middle_finger_pip.y and 
                              middle_finger_pip.y < middle_finger_mcp.y)

    # Condition 3: Ensure ring and pinky fingers are down
    ring_finger_down = ring_finger_tip.y > ring_finger_mcp.y
    pinky_down = pinky_tip.y > pinky_mcp.y

    # Both index and middle fingers should be extended, while ring and pinky are down
    return index_finger_extended and middle_finger_extended and ring_finger_down and pinky_down


def is_index_finger_up(mp_hands, hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    
    # Condition 1: Check if index finger is extended (tip is higher than other joints)
    index_finger_extended = (index_finger_tip.y < index_finger_dip.y and 
                             index_finger_dip.y < index_finger_pip.y and 
                             index_finger_pip.y < index_finger_mcp.y)

    # Condition 2: Ensure that other fingers are not extended
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    
    other_fingers_down = (middle_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y and
                          ring_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y and
                          pinky_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y)

    return index_finger_extended and other_fingers_down