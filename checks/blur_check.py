import cv2

def check_blur(image_path, threshold=40):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    score = cv2.Laplacian(gray, cv2.CV_64F).var()
    if score < threshold:
        return True, f"IMAGE BLURRY — Please retake with a clearer image (score: {score:.1f})"
    return False, f"Image is clear (score: {score:.1f})"