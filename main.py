import os
from checks.face_detect   import detect_face
from checks.blur_check    import check_blur
from checks.mask_check    import check_mask
from checks.glasses_check import check_glasses

def kyc_check(image_path):
    print("\n" + "="*45)
    print(f"  KYC CHECK: {image_path}")
    print("="*45)
    results = {}

    face_ok, face_msg, face_coords = detect_face(image_path)
    results['face'] = {'status': face_ok, 'message': face_msg}
    print(f"[1] Face:    {'PASS' if face_ok else 'FAIL'} — {face_msg}")

    if not face_ok:
        print("="*45)
        print("  FINAL: KYC REJECTED")
        print("="*45)
        results['final'] = False
        return results

    blurry, blur_msg = check_blur(image_path)
    results['blur'] = {'status': not blurry, 'message': blur_msg}
    print(f"[2] Blur:    {'FAIL' if blurry else 'PASS'} — {blur_msg}")

    masked, mask_msg = check_mask(image_path, face_coords)
    results['mask'] = {'status': not masked, 'message': mask_msg}
    print(f"[3] Mask:    {'FAIL' if masked else 'PASS'} — {mask_msg}")

    glasses, g_msg = check_glasses(image_path, face_coords)
    results['glasses'] = {'status': not glasses, 'message': g_msg}
    print(f"[4] Glasses: {'FAIL' if glasses else 'PASS'} — {g_msg}")

    all_ok = face_ok and not blurry and not masked and not glasses
    print("="*45)
    print(f"  FINAL: {'KYC APPROVED' if all_ok else 'KYC REJECTED'}")
    print("="*45)
    results['final'] = all_ok
    return results

if __name__ == "__main__":
    kyc_check("uploads/test.jpg")
    