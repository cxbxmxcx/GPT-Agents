import cv2
import time
from datetime import datetime

def capture_images(interval, duration):
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is typically the default value for the first webcam
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time > duration:
            break

        # Capture a single frame
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Create a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}.png"

        # Save the captured image with the timestamp
        cv2.imwrite(filename, frame)

        # Wait for the specified interval
        time.sleep(interval)

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

# Usage
capture_images(interval=5, duration=10)  # Capture an image every 5 seconds for 1 minute
