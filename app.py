import cv2
import mediapipe as mp
import pygame
import time
import numpy as np
from collections import deque

# Initialize pygame for alarm
pygame.mixer.init()

# Low lighting enhancement
def enhance_brightness_contrast(frame):
    """
    Enhances brightness and contrast for low-light conditions.
    """
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
    frame_enhanced = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    return frame_enhanced

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 387, 385, 263, 373, 380]

# Parameters
CLOSED_THRESHOLD = 1.2    # seconds before alarm
closed_start_time = None
alarm_playing = False

# Smoothing
eye_history = deque(maxlen=5)

# Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("=" * 60)
print("MEDIAPIPE DROWSINESS DETECTION")
print("=" * 60)
print("Press 'q' to quit")

# Pre-load the alarm once at the start
alarm_sound = pygame.mixer.Sound("alarm.mp3")
alarm_sound.set_volume(1.0)

def play_alarm():
    global alarm_playing
    if not alarm_playing:
        alarm_sound.play(loops=-1)  # loop indefinitely
        alarm_playing = True
        print("🔴 ALARM - EYES CLOSED!")

def stop_alarm():
    global alarm_playing
    if alarm_playing:
        alarm_sound.stop()
        alarm_playing = False
        print("✅ Alarm stopped")

# Function to calculate vertical eye distance
def eye_open_ratio(landmarks, eye_points, h):
    upper = np.mean([landmarks[eye_points[1]].y, landmarks[eye_points[2]].y])
    lower = np.mean([landmarks[eye_points[4]].y, landmarks[eye_points[5]].y])
    vertical_distance = (lower - upper) * h
    return vertical_distance

# FPS calculation
fps = 0
frame_count = 0
fps_start = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # FPS
    frame_count += 1
    if time.time() - fps_start >= 1.0:
        fps = frame_count
        frame_count = 0
        fps_start = time.time()

    # Enhance frame for low-light
    frame_enhanced = enhance_brightness_contrast(frame)
    rgb_frame = cv2.cvtColor(frame_enhanced, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        h, w = frame.shape[:2]
        landmarks = results.multi_face_landmarks[0].landmark

        # Calculate vertical eye distances (pixels)
        left_eye_dist = eye_open_ratio(landmarks, LEFT_EYE, h)
        right_eye_dist = eye_open_ratio(landmarks, RIGHT_EYE, h)
        avg_eye_dist = (left_eye_dist + right_eye_dist) / 2.0

        # Smooth eye distance
        eye_history.append(avg_eye_dist)
        smoothed_eye = np.mean(eye_history)

        # Dynamic threshold relative to eye size
        eye_dist_threshold = max(5, 0.4 * smoothed_eye)
        eyes_open = smoothed_eye > eye_dist_threshold

        # Visual feedback
        if eyes_open:
            cv2.putText(frame, "EYES OPEN", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (50, 80), (250, 130), (0, 255, 0), 2)
        else:
            cv2.putText(frame, "EYES CLOSED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.rectangle(frame, (50, 80), (250, 130), (0, 0, 255), 2)

        cv2.putText(frame, f"Eye dist: {smoothed_eye:.2f}", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"FPS: {fps}", (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Alarm logic
        current_time = time.time()
        if not eyes_open:
            if closed_start_time is None:
                closed_start_time = current_time
            elif current_time - closed_start_time >= CLOSED_THRESHOLD:
                play_alarm()
        else:
            if closed_start_time is not None:
                closed_start_time = None
                stop_alarm()
    else:
        cv2.putText(frame, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"FPS: {fps}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Drowsiness Detection - Press 'q'", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        stop_alarm()
        break

cap.release()
cv2.destroyAllWindows()
print("\nSystem shutdown complete")