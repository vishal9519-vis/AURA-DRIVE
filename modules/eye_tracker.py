# ============================================================
#  AURA DRIVE — modules/eye_tracker.py
#  EAR (Eye Aspect Ratio) calculation + blink counting
# ============================================================

from scipy.spatial import distance as dist
from imutils import face_utils
import cv2
from config import Config


# dlib 68-point landmark indices for left and right eye
(L_START, L_END) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_START, R_END) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


def eye_aspect_ratio(eye):
    """
    Compute the Eye Aspect Ratio (EAR) for a single eye.

    EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)

    Returns float. EAR < Config.EAR_THRESHOLD → eyes closed.
    """
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


def get_ear(landmarks):
    """Compute average EAR across both eyes from 68-landmark array."""
    left_eye  = landmarks[L_START:L_END]
    right_eye = landmarks[R_START:R_END]
    left_ear  = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    return (left_ear + right_ear) / 2.0, left_eye, right_eye


def draw_eyes(frame, left_eye, right_eye):
    """Draw eye contours on the frame."""
    import cv2
    from imutils import face_utils
    left_hull  = cv2.convexHull(left_eye)
    right_hull = cv2.convexHull(right_eye)
    cv2.drawContours(frame, [left_hull],  -1, Config.COLOR_GREEN, 1)
    cv2.drawContours(frame, [right_hull], -1, Config.COLOR_GREEN, 1)
