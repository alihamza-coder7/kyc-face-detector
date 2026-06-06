import cv2
import numpy as np

def check_glasses(image_path, face_coords):
    img = cv2.imread(image_path)
    x, y, w, h = face_coords
    eye_y_start = y + int(h * 0.15)
    eye_y_end   = y + int(h * 0.45)
    eye_region  = img[eye_y_start:eye_y_end, x : x + w]
    gray_eye    = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
    brightness  = np.mean(gray_eye)
    dark_pixels = np.sum(gray_eye < 80)
    dark_percent = (dark_pixels / gray_eye.size) * 100
    if dark_percent > 35 and brightness < 90:
        return True, f"SUNGLASSES DETECTED — KYC DECLINED (dark: {dark_percent:.1f}%)"
    return False, f"No glasses — KYC APPROVED (dark: {dark_percent:.1f}%)"