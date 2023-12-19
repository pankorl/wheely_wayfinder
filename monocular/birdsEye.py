import cv2
import numpy as np

def perform_birds_eye_transformation(image, pts1, pts2, width, height):
    # Get the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Perform the perspective warp
    bird_eye_view = cv2.warpPerspective(image, matrix, (width, height))

    return bird_eye_view