# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 12:12:45 2024

@author: Morteza
"""

import cv2
import numpy as np
import math

# Video settings
frame_width = 1920
frame_height = 1080
num_frames = 600  # For 20 seconds at 30 fps

# Create a window
cv2.namedWindow('Sinusoidal Circle Relation', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Sinusoidal Circle Relation', frame_width, frame_height)

# Initialize point positions
point_on_sin_x = (0, frame_height // 2)
point_on_cos_x = (frame_width // 2, 0)

# Initial angle for the point on the circle (to start at the top of the circle)
initial_angle = -math.pi / 2
angle_increment = 2 * math.pi / num_frames  # Adjusted increment for equal speed

# Calculate increment for movement along the sinusoidal curves
sinusoidal_increment_x = frame_width / num_frames
sinusoidal_increment_y = frame_height / num_frames

# Infinite loop
while True:
    for frame_idx in range(num_frames):
        # Create blank frame
        frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

        # Draw axes
        axis_color = (255, 255, 255)
        cv2.line(frame, (0, frame_height // 2), (frame_width, frame_height // 2), axis_color, 2)
        cv2.line(frame, (frame_width // 2, 0), (frame_width // 2, frame_height), axis_color, 2)

        # Draw unit circle
        circle_center = (frame_width // 2, frame_height // 2)
        circle_radius = min(frame_width, frame_height) // 3
        cv2.circle(frame, circle_center, circle_radius, (255, 255, 255), 2)

        # Calculate point on unit circle
        angle = initial_angle + frame_idx * angle_increment
        point_on_circle = (int(circle_center[0] + circle_radius * math.cos(angle)),
                           int(circle_center[1] + circle_radius * math.sin(angle)))

        # Draw point on unit circle
        cv2.circle(frame, point_on_circle, 20, (0, 255, 255), -1)  # Larger point size

        # Draw line from center to point on unit circle
        cv2.line(frame, circle_center, point_on_circle, (0, 255, 255), 2)

        # Draw Cos(x) curve (horizontal)
        cos_x_curve = [(x, frame_height // 2 + int(frame_height / 4 * math.cos(2 * math.pi * (x - frame_width // 2) / frame_width))) for x in range(frame_width)]
        cv2.polylines(frame, [np.array(cos_x_curve)], False, (0, 255, 0), 2)

        # Draw Sin(x) curve (vertical)
        sin_x_curve = [(frame_width // 2 + int(frame_width / 4 * math.sin(2 * math.pi * (y - frame_height // 2) / frame_height)), y) for y in range(frame_height)]
        cv2.polylines(frame, [np.array(sin_x_curve)], False, (255, 0, 0), 2)

        # Update point position on Sin(x) curve (vertical)
        point_on_sin_x = (frame_width // 2 + int(frame_width / 4 * math.sin(2 * math.pi * (frame_idx * sinusoidal_increment_y - frame_height // 2) / frame_height)), int(frame_idx * sinusoidal_increment_y))

        # Draw moving point on Sin(x) curve (vertical)
        cv2.circle(frame, point_on_sin_x, 15, (0, 0, 255), -1)  # Larger point size

        # Update point position on Cos(x) curve (horizontal)
        point_on_cos_x = (int(frame_idx * sinusoidal_increment_x), frame_height // 2 + int(frame_height / 4 * math.cos(2 * math.pi * (frame_idx * sinusoidal_increment_x - frame_width // 2) / frame_width)))

        # Draw moving point on Cos(x) curve (horizontal)
        cv2.circle(frame, point_on_cos_x, 15, (255, 255, 0), -1)  # Larger point size

        # Display frame
        cv2.imshow('Sinusoidal Circle Relation', frame)

        # Check if points reached the end of curves, reset if necessary
        if frame_idx == num_frames - 1:
            frame_idx = 0

        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    # Reset point positions
    point_on_sin_x = (0, frame_height // 2)
    point_on_cos_x = (frame_width // 2, 0)

# Release window
cv2.destroyAllWindows()
