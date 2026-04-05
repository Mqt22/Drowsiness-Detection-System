# Drowsiness-Detection-System
Developer: Abdul Muqeet

**Overview**

The Drowsiness Detection System is an intelligent real-time monitoring tool designed to detect when a person’s eyes are closed, indicating possible drowsiness or sleep. Using advanced computer vision technology with MediaPipe and OpenCV, this system is perfect for scenarios like driving, studying, or working, where maintaining alertness is crucial.

The system continuously monitors the user through a webcam (or smartphone camera via apps like iVCam) and triggers an immediate alarm when closed eyes are detected for a set duration. This ensures maximum safety and awareness, especially in low-light conditions.

**Key Features**
**Real-Time Eye Monitoring**
Detects if eyes are open or closed with high accuracy.
Provides continuous feedback using eye distance calculations.
**Immediate Alarm Notification**
Plays a loud alarm sound when eyes are closed beyond a preset threshold (default 1.2 seconds).
Alarm loops continuously until eyes are detected as open.
**Visual Feedback**
Shows a clear on-screen rectangle indicating eye state: green for open, red for closed.
Displays “EYES OPEN” or “EYES CLOSED” text for easy recognition.
**Low-Light Adaptation**
Enhances webcam footage in dim lighting to improve detection accuracy.
Can be used in environments with minimal light, such as inside a car at night.
**Smooth Detection**
Uses a moving average to reduce false alarms from blinking.
Calculates dynamic thresholds relative to face size for adaptability to different users.
**Performance Metrics**
Displays real-time FPS (Frames Per Second) and eye distance for transparency.
Works smoothly on standard laptops and PCs.
**Cross-Device Support**
Can use a Windows laptop webcam or an iPhone/Android camera via apps like iVCam.
**Known Limitations / Bugs**
Light sensitivity: Detection may be less accurate in extremely dark conditions. Low-light enhancement improves performance, but extremely poor lighting may still affect accuracy.
Camera distance: If the user is too far from the camera, detection may be less reliable. Best performance is at a normal sitting distance (50–100 cm).
False positives: Very fast blinking or partial eye closure can occasionally trigger the alarm.
**How to Use
Setup:**
Install Python and required libraries (OpenCV, MediaPipe, Pygame, Numpy).
Ensure a webcam or smartphone camera (via iVCam) is ready.
**Run the System:**
Launch the program. A live camera feed window will appear.
The system will automatically detect your face and track eye movements.
**Interpret Feedback:**
Green rectangle + "EYES OPEN": Eyes are open; no alarm.
Red rectangle + "EYES CLOSED": Eyes are closed; alarm will trigger after 1.2 seconds.
Alarm sound: Stops automatically when eyes reopen.
**Exit:**
Press 'q' to quit the system safely.
**Why Use This System?**
Provides an affordable and effective solution for monitoring alertness.
Works in real-time, ideal for drivers, students, and night-shift workers.
Easy to set up and run, even for non-technical users.
Lightweight and fast, adaptable to different devices and lighting conditions.
