import cv2
import mediapipe as mp
import numpy as np
import math
import time
import json
import os

# Ensure database folder exists
os.makedirs("./database", exist_ok=True)

# File path for workout history
WORKOUT_HISTORY_PATH = "./database/workout_history.json"

# Initialize MediaPipe Pose Estimation
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Define exercise landmark mappings and calorie burn per rep
WORKOUTS = {
    "Bicep Curls": (11, 13, 15),  # Shoulder, Elbow, Wrist
    "Squats": (24, 26, 28),       # Hip, Knee, Ankle
    "Push-ups": (12, 14, 16),     # Shoulder, Elbow, Wrist
    "Lunges": (24, 26, 28),       # Hip, Knee, Ankle
    "Deadlifts": (24, 26, 28),    # Hip, Knee, Ankle
    "Planks": (12, 14, 16),       # Shoulder, Elbow, Wrist
    "Bench Press": (12, 14, 16)   # Shoulder, Elbow, Wrist
}

CALORIES_PER_REP = {
    "Bicep Curls": 0.5,
    "Squats": 0.8,
    "Push-ups": 0.7,
    "Lunges": 0.6,
    "Deadlifts": 1.2,
    "Planks": 0.3,
    "Bench Press": 1.0
}

def findAngle(img, lmList, p1, p2, p3, draw=True):
    """Calculate the angle between three key points."""
    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    x3, y3 = lmList[p3][1:]
    
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360
    
    if draw:
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
        cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
        cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    
    return angle


