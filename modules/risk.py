# ============================================================
#  AURA DRIVE — modules/risk.py
#  Risk score computation + adaptive safety response
# ============================================================

from config import Config
from modules.emotion import emotion_risk_bonus


def compute_risk(attention_score, fatigue_level, emotion, is_distracted):
    """
    Compute 0–100 risk score.

    Risk = (100 - attention) × 0.4 + fatigue × 0.4
         + emotion_bonus + distraction_bonus
    Clamped to [0, 100].
    """
    risk = (
        (100 - attention_score) * Config.RISK_WEIGHT_ATTENTION
        + fatigue_level         * Config.RISK_WEIGHT_FATIGUE
        + emotion_risk_bonus(emotion)
        + (Config.RISK_ADD_DISTRACTED if is_distracted else 0)
    )
    return min(100.0, max(0.0, risk))


def adaptive_response(risk_score):
    """
    Return (level, message, color) based on risk score.

    Levels:
        SAFE      → risk < 25
        CAUTION   → 25 ≤ risk < 50
        WARNING   → 50 ≤ risk < 75
        EMERGENCY → risk ≥ 75
    """
    if risk_score < 25:
        return "SAFE",      "✅ Drive safely. All systems normal.",          Config.COLOR_GREEN
    elif risk_score < 50:
        return "CAUTION",   "⚠️  Caution: monitor your alertness.",          Config.COLOR_YELLOW
    elif risk_score < 75:
        return "WARNING",   "🚨 WARNING: Take a break soon!",                Config.COLOR_ORANGE
    else:
        return "EMERGENCY", "🛑 EMERGENCY: Pull over NOW! High risk detected!", Config.COLOR_RED


def update_attention(attention_score, ear, is_distracted, mar):
    """
    Update 0–100 attention score for the current frame.
    Drops on fatigue/distraction signals, recovers otherwise.
    """
    if ear < Config.EAR_THRESHOLD:
        attention_score -= Config.ATTENTION_DROP_EYE
    elif is_distracted:
        attention_score -= Config.ATTENTION_DROP_DISTRACTED
    elif mar > Config.MAR_THRESHOLD:
        attention_score -= Config.ATTENTION_DROP_YAWN
    else:
        attention_score += Config.ATTENTION_RECOVER
    return min(100.0, max(0.0, attention_score))
