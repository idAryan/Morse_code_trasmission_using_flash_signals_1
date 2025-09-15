# =============================
# STEP 1: Imports
# =============================
import cv2
import numpy as np
import time

# =============================
# STEP 2: Morse Dictionary
# =============================
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9'
}

# =============================
# STEP 3: Circle + Light Detection
# =============================
def create_circular_mask(frame, radius=100):
    height, width = frame.shape[:2]
    center = (width // 2, height // 2)
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    return mask, center, radius

def detect_light_in_circle(frame, mask, brightness_threshold=240, area_threshold=300):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    masked_gray = cv2.bitwise_and(gray, gray, mask=mask)
    blurred = cv2.GaussianBlur(masked_gray, (5, 5), 0)
    _, bright_spots = cv2.threshold(blurred, brightness_threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(bright_spots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > area_threshold:
            return True, contour
    return False, None

def decode_morse_to_english(morse_code):
    return MORSE_CODE_DICT.get(morse_code, '?')

# =============================
# STEP 4: Main Morse Processing Loop (Jupyter/PC Version)
# =============================
def run_morse_detector():
    cap = cv2.VideoCapture(0)   # webcam open
    if not cap.isOpened():
        print("❌ Cannot access webcam")
        return

    # Morse timing (seconds)
    DIT_MAX_DURATION = 0.3
    LETTER_GAP = 0.7
    WORD_GAP = 1.4

    current_morse = ""
    decoded_text = ""
    last_light_state = False
    light_start_time = 0
    last_light_end_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        mask, center, radius = create_circular_mask(frame)
        light_detected, contour = detect_light_in_circle(frame, mask)

        current_time = time.time()

        # Handle state changes
        if light_detected != last_light_state:
            if light_detected:
                light_start_time = current_time
            else:
                duration = current_time - light_start_time
                current_morse += "." if duration < DIT_MAX_DURATION else "-"
                last_light_end_time = current_time
            last_light_state = light_detected

        # Letter gap
        elif not light_detected and current_morse and (current_time - last_light_end_time) > LETTER_GAP:
            decoded_text += decode_morse_to_english(current_morse)
            current_morse = ""
            last_light_end_time = current_time

        # Word gap
        elif not light_detected and decoded_text and (current_time - last_light_end_time) > WORD_GAP:
            if not decoded_text.endswith(" "):
                decoded_text += " "
            last_light_end_time = current_time

        # Overlay visuals
        cv2.circle(frame, center, radius, (255, 0, 0), 2)
        if light_detected and contour is not None:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

        status_text = "Flash Detected!" if light_detected else "No Flash"
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0) if light_detected else (0, 0, 255), 2)
        cv2.putText(frame, f"Morse: {current_morse}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
        cv2.putText(frame, f"Decoded: {decoded_text[-30:]}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.imshow("Morse Detector", frame)

        # Quit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# =============================
# STEP 5: Run Detector
# =============================
run_morse_detector()