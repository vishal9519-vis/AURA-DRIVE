# ============================================================
#  AURA DRIVE — modules/face_detection.py
#  dlib face detection + 68-point landmark prediction
# ============================================================

import dlib
import cv2
from imutils import face_utils
from config import Config

# Lazy init — detector created on first use so import never crashes
_detector  = None
_predictor = None


def _get_detector():
    global _detector
    if _detector is None:
        _detector = dlib.get_frontal_face_detector()
    return _detector


def load_predictor(model_path="shape_predictor_68_face_landmarks.dat"):
    """Load dlib's 68-point landmark predictor."""
    global _predictor
    _predictor = dlib.shape_predictor(model_path)
    print(f"[face_detection] Predictor loaded from: {model_path}")


def detect_faces(gray_frame):
    """Return list of dlib face rectangles detected in a grayscale frame."""
    return _get_detector()(gray_frame, 0)


def get_landmarks(gray_frame, face_rect):
    """Return 68 facial landmark (x, y) coordinates as a NumPy array."""
    if _predictor is None:
        raise RuntimeError("Predictor not loaded. Call load_predictor() first.")
    shape = _predictor(gray_frame, face_rect)
    return face_utils.shape_to_np(shape)


def draw_face_box(frame, face_rect, color=None):
    """Draw a bounding box around a detected face."""
    color = color or Config.COLOR_GREEN
    (x, y, w, h) = face_utils.rect_to_bb(face_rect)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


def draw_landmarks(frame, landmarks, color=None):
    """Draw all 68 landmark dots on the frame."""
    color = color or Config.COLOR_CYAN
    for (x, y) in landmarks:
        cv2.circle(frame, (x, y), 1, color, -1)
