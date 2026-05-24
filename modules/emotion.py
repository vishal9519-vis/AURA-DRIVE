# ============================================================
#  AURA DRIVE — modules/emotion.py
#  Rule-based emotion detection from facial geometry signals
#  States: CALM | FOCUSED | STRESSED | TIRED | YAWNING
# ============================================================

from config import Config


def detect_emotion(ear, mar, fatigue_level, attention_score):
    """
    Classify driver emotional state using threshold rules.

    Priority order: YAWNING > TIRED > STRESSED > FOCUSED > CALM
    Returns emotion label string.
    """
    if mar > Config.MAR_THRESHOLD:
        return "YAWNING"
    if ear < Config.EAR_THRESHOLD or fatigue_level > 60:
        return "TIRED"
    if attention_score < 50:
        return "STRESSED"
    if attention_score >= 75:
        return "FOCUSED"
    return "CALM"


# Emoji/display mapping for the dashboard overlay
EMOTION_DISPLAY = {
    "CALM":    ("😌 CALM",    (0, 220, 80)),
    "FOCUSED": ("🎯 FOCUSED", (255, 220, 0)),
    "STRESSED":("😟 STRESSED",(0, 130, 200)),
    "TIRED":   ("😴 TIRED",   (0, 200, 255)),
    "YAWNING": ("🥱 YAWNING", (0, 40, 220)),
}


def emotion_risk_bonus(emotion):
    """Extra risk points added based on current emotion."""
    return {
        "TIRED":    Config.RISK_ADD_TIRED,
        "STRESSED": Config.RISK_ADD_STRESSED,
        "YAWNING":  Config.RISK_ADD_YAWNING,
    }.get(emotion, 0)
