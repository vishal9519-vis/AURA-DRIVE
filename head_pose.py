# ============================================================
#  AURA DRIVE — modules/head_pose.py
#  Head pose estimation (pitch, yaw, roll) via solvePnP
# ============================================================

import numpy as np
import cv2
from config import Config


# 3D model points for a generic face (mm scale)
MODEL_POINTS = np.array([
    (0.0,    0.0,    0.0),    # Nose tip           — landmark 30
    (0.0,   -330.0, -65.0),   # Chin               — landmark  8
    (-225.0, 170.0, -135.0),  # Left eye corner    — landmark 36
    (225.0,  170.0, -135.0),  # Right eye corner   — landmark 45
    (-150.0, -150.0,-125.0),  # Left mouth corner  — landmark 48
    (150.0,  -150.0,-125.0),  # Right mouth corner — landmark 54
], dtype=np.float64)

LANDMARK_IDX = [30, 8, 36, 45, 48, 54]


def get_camera_matrix(frame_width, frame_height):
    focal = frame_width
    center = (frame_width / 2, frame_height / 2)
    return np.array([
        [focal, 0,     center[0]],
        [0,     focal, center[1]],
        [0,     0,     1        ]
    ], dtype=np.float64)


def estimate_head_pose(landmarks, frame_shape):
    """
    Estimate head pose using solvePnP.
    Returns (yaw, pitch, roll) in degrees, or (0, 0, 0) on failure.
    """
    h, w = frame_shape[:2]
    image_points = np.array(
        [landmarks[i] for i in LANDMARK_IDX], dtype=np.float64
    )
    camera_matrix = get_camera_matrix(w, h)
    dist_coeffs = np.zeros((4, 1))

    success, rot_vec, _ = cv2.solvePnP(
        MODEL_POINTS, image_points, camera_matrix, dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE
    )
    if not success:
        return 0.0, 0.0, 0.0

    rot_mat, _ = cv2.Rodrigues(rot_vec)
    # Decompose into Euler angles (degrees)
    sy = np.sqrt(rot_mat[0, 0] ** 2 + rot_mat[1, 0] ** 2)
    pitch = np.degrees(np.arctan2(-rot_mat[2, 0], sy))
    yaw   = np.degrees(np.arctan2(rot_mat[1, 0], rot_mat[0, 0]))
    roll  = np.degrees(np.arctan2(rot_mat[2, 1], rot_mat[2, 2]))
    return yaw, pitch, roll


def is_distracted(yaw, pitch):
    """Return True if head is turned/tilted beyond thresholds."""
    return (abs(yaw)   > Config.YAW_THRESHOLD or
            abs(pitch) > Config.PITCH_THRESHOLD)
