# ============================================================
#  AURA DRIVE — config.py
#  Central configuration — all thresholds and settings
# ============================================================

class Config:

    # ── Project Info ─────────────────────────────────────────
    PROJECT_NAME = "AURA DRIVE"
    VERSION      = "1.0.0"
    DESCRIPTION  = "AI-Powered Adaptive Driver Intelligence & Safety System"

    # ── Detection Thresholds ─────────────────────────────────
    EAR_THRESHOLD   = 0.22   # Eye Aspect Ratio — below = eyes closed
    MAR_THRESHOLD   = 0.55   # Mouth Aspect Ratio — above = yawning
    CONSEC_FRAMES   = 15     # Consecutive frames before fatigue alert

    # ── Head Pose Thresholds (degrees) ───────────────────────
    YAW_THRESHOLD   = 25     # Left/right head turn = distracted
    PITCH_THRESHOLD = 20     # Up/down head tilt = distracted

    # ── Session Settings ─────────────────────────────────────
    WEBCAM_WIDTH    = 640
    WEBCAM_HEIGHT   = 480
    WEBCAM_QUALITY  = 0.92
    CAPTURE_DELAY   = 1.5    # seconds between frames

    # ── Scoring Weights ──────────────────────────────────────
    ATTENTION_DROP_EYE        = 3.0
    ATTENTION_DROP_DISTRACTED = 2.5
    ATTENTION_DROP_YAWN       = 1.5
    ATTENTION_RECOVER         = 0.8

    FATIGUE_INC_EYE      = 2.0
    FATIGUE_INC_YAWN     = 1.5
    FATIGUE_INC_DISTRACT = 0.5
    FATIGUE_INC_EMOTION  = 1.0
    FATIGUE_SCALE        = 0.3

    # ── Risk Weights ─────────────────────────────────────────
    RISK_WEIGHT_ATTENTION = 0.4
    RISK_WEIGHT_FATIGUE   = 0.4
    RISK_ADD_TIRED        = 15
    RISK_ADD_STRESSED     = 10
    RISK_ADD_YAWNING      = 8
    RISK_ADD_DISTRACTED   = 10

    # ── Safety Score Penalties ───────────────────────────────
    PENALTY_FATIGUE_ALERT    = 8
    PENALTY_YAWN             = 5
    PENALTY_DISTRACTION      = 6
    PENALTY_HIGH_FATIGUE     = 10
    PENALTY_LOW_ATTENTION    = 10

    # ── Display Colors (BGR) ─────────────────────────────────
    COLOR_GREEN  = (0, 220,  80)
    COLOR_YELLOW = (0, 200, 255)
    COLOR_RED    = (0,  40, 220)
    COLOR_ORANGE = (0, 130, 200)
    COLOR_CYAN   = (255, 220, 0)
    COLOR_WHITE  = (255, 255, 255)
    COLOR_DARK   = (15,  15,  15)
