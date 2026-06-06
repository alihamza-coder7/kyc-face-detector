import cv2
import numpy as np

def check_mask(image_path, face_coords):
    # Load fresh image — already rotated
    img = cv2.imread(image_path)
    
    if img is None:
        return False, "No mask — Image could not be loaded"

    img_h, img_w = img.shape[:2]
    x, y, w, h = face_coords

    # Keep coordinates within image bounds
    x = max(0, min(x, img_w - 1))
    y = max(0, min(y, img_h - 1))
    w = min(w, img_w - x)
    h = min(h, img_h - y)

    if w < 10 or h < 10:
        return False, "No mask — Face area too small"

    # Lower face crop — nose and mouth region
    lower_y = y + int(h * 0.45)
    lower_h = y + h
    lower_face = img[lower_y:lower_h, x:x+w]

    if lower_face.size == 0:
        return False, "No mask — Face is clear"

    # Convert to HSV
    hsv = cv2.cvtColor(lower_face, cv2.COLOR_BGR2HSV)

    # Skin color ranges
    masks = [
        cv2.inRange(hsv, np.array([0,  15, 50],  dtype=np.uint8), np.array([25, 255, 255], dtype=np.uint8)),
        cv2.inRange(hsv, np.array([0,  10, 60],  dtype=np.uint8), np.array([20, 200, 255], dtype=np.uint8)),
        cv2.inRange(hsv, np.array([0,  20, 70],  dtype=np.uint8), np.array([20, 255, 255], dtype=np.uint8)),
    ]
    combined = masks[0]
    for m in masks[1:]:
        combined = cv2.bitwise_or(combined, m)

    skin_percent = (np.sum(combined > 0) / combined.size) * 100

    if skin_percent < 20:
        return True, f"MASK DETECTED — Please remove your mask (skin: {skin_percent:.1f}%)"

    return False, f"No mask — Face is clear (skin: {skin_percent:.1f}%)"