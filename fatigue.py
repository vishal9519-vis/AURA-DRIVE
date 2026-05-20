# ============================================================
#  AURA DRIVE — modules/fatigue.py
#  MAR (Mouth Aspect Ratio) + cumulative fatigue tracking
# ============================================================

from scipy.spatial import distance as dist
from imutils import face_utils
import cv2
from config import Config


(M_START, M_END) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]


def mouth_aspect_ratio(mouth):
    """
    Compute the Mouth Aspect Ratio (MAR).

    MAR = (||v1|| + ||v2|| + ||v3||) / (2 * ||h||)

    MAR > Config.MAR_THRESHOLD → yawning.
    """
    A = dist.euclidean(mouth[2],  mouth[10])  # vertical 1
    B = dist.euclidean(mouth[4],  mouth[8])   # vertical 2
    C = dist.euclidean(mouth[0],  mouth[6])   # horizontal
    return (A + B) / (2.0 * C)


def get_mar(landmarks):
    """Return MAR and the mouth landmark array."""
    mouth = landmarks[M_START:M_END]
    return mouth_aspect_ratio(mouth), mouth


def update_fatigue(fatigue_level, ear, mar, emotion, is_distracted):
    """
    Accumulate fatigue based on current frame signals.
    Fatigue only increases — never resets during a session.
    Returns updated fatigue_level (float, clamped 0–100).
    """
    delta = 0.0
    if ear < Config.EAR_THRESHOLD:
        delta += Config.FATIGUE_INC_EYE
    if mar > Config.MAR_THRESHOLD:
        delta += Config.FATIGUE_INC_YAWN
    if is_distracted:
        delta += Config.FATIGUE_INC_DISTRACT
    if emotion in ("TIRED", "STRESSED"):
        delta += Config.FATIGUE_INC_EMOTION
    fatigue_level += delta * Config.FATIGUE_SCALE
    return min(100.0, fatigue_level)
