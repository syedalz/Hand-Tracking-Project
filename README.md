# Hand-Tracking Project

A real-time computer vision project that uses hand gestures to control the system’s master volume. The distance between the thumb and index finger is tracked using MediaPipe hand landmarks and mapped directly to Windows system volume levels.

---

## Overview

This project combines OpenCV, MediaPipe, and Windows Core Audio to demonstrate real-time gesture-based interaction. A webcam is used to detect hand landmarks, calculate finger distance, and dynamically adjust system volume with visual feedback.

---

## Features

- Real-time hand detection via webcam
- 21-point hand landmark tracking
- Gesture-based system volume control
- Smooth volume interpolation
- Visual volume bar and percentage display
- FPS counter for performance monitoring
- Direct Windows Core Audio integration (Pycaw)

---

## Technologies Used

- Python 3
- OpenCV
- MediaPipe
- NumPy
- Pycaw
- ctypes / comtypes

---


## Project Structure

Hand-Tracking Project/
├── HandTrackingModule.py
├── VolumeControl.py
└── README.md

yaml
Copy code

---

## Installation

Install the required dependencies:

in bash terminal:
pip install opencv-python mediapipe numpy pycaw comtypes


## How to Run

Ensure a webcam is connected.

Navigate to the project directory.

Run the main program:

python VolumeControl.py



## How It Works

MediaPipe detects hand landmarks from webcam frames.

Thumb tip (ID 4) and index finger tip (ID 8) are tracked.

The distance between these landmarks is calculated.

This distance is interpolated to match system volume levels.

Windows Core Audio is accessed through Pycaw to update volume.

Visual feedback is displayed in real time.

## Learning Outcomes

Computer vision fundamentals

MediaPipe hand landmark indexing

Real-time gesture recognition

Mapping physical gestures to system actions

Interfacing with Windows Core Audio using COM

Modular Python project design

## Project Structure

