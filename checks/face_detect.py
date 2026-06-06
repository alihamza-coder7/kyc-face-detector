import cv2

def detect_face(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return False, "FACE NOT PRESENT — Image could not be loaded", None

    front_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml')

    rotations = [
        img,
        cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
        cv2.rotate(img, cv2.ROTATE_180),
        cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    ]

    best_rotated = None
    best_face = None

    for rotated in rotations:
        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        img_h, img_w = rotated.shape[:2]
        img_area = img_h * img_w

        faces = front_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

        if len(faces) == 0:
            eyes = eye_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=8, minSize=(40, 40))
            if len(eyes) >= 2:
                eyes = sorted(eyes, key=lambda e: e[2]*e[3], reverse=True)
                ex, ey, ew, eh = eyes[0]
                fx = max(0, ex - ew)
                fy = max(0, ey - eh*2)
                fw = min(ew * 4, img_w - fx)
                fh = min(eh * 6, img_h - fy)
                # Save rotated image first
                cv2.imwrite(image_path, rotated)
                return True, "Face detected successfully!", (fx, fy, fw, fh)
            continue

        faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
        main_face = faces[0]
        main_area = main_face[2] * main_face[3]

        if main_area < img_area * 0.02:
            continue

        real_faces = [f for f in faces if (f[2]*f[3]) > main_area * 0.3]

        if len(real_faces) > 1:
            return False, "REJECTED — Multiple faces detected, please take a solo photo", None

        best_rotated = rotated
        best_face = main_face
        break

    if best_face is None:
        return False, "FACE NOT PRESENT — No face found in the photo", None

    # Save rotated image then return coords
    cv2.imwrite(image_path, best_rotated)
    x, y, w, h = best_face
    return True, "Face detected successfully!", (x, y, w, h)