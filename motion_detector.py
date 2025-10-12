import cv2
import time
from alert_logger import send_sms, log_event  # Import your alert functions

def detect_motion():
    cap = cv2.VideoCapture(0)  # Open webcam
    time.sleep(2)  # Warm up camera

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    last_alert_time = 0
    alert_cooldown = 60  # seconds between alerts

    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)  # Difference between frames
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue  # Ignore small movements
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        current_time = time.time()
        if motion_detected and (current_time - last_alert_time) > alert_cooldown:
            print("Motion Detected! Sending alert...")
            send_sms("Alert! Motion detected in front of the camera.")
            log_event("Motion detected")
            last_alert_time = current_time

        cv2.imshow("Motion Detector", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(10) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_motion()
