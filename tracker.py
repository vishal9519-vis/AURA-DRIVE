# ============================================================
#  AURA DRIVE — modules/tracker.py
#  AuraTracker — central session state manager
# ============================================================

import pandas as pd
from datetime import datetime
from config import Config


class AuraTracker:
    """
    Manages all per-session state: scores, logs, counters.
    Instantiate once per driving session.
    """

    def __init__(self):
        self.session_start   = datetime.now()
        self.frame_count     = 0
        self.blink_count     = 0
        self.yawn_count      = 0
        self.fatigue_alerts  = 0
        self.consec_closed   = 0  # consecutive frames with EAR < threshold

        # Running scores
        self.attention_score = 100.0
        self.fatigue_level   = 0.0
        self.risk_score      = 0.0
        self.safety_score    = 100.0

        # Per-frame history for dashboard
        self.log = []  # list of dicts → converted to DataFrame at end

    # ── Per-frame update ──────────────────────────────────────

    def update(self, ear, mar, yaw, pitch, roll,
               emotion, attention, fatigue, risk, response_level):
        """Record one frame's data into the session log."""
        self.frame_count    += 1
        self.attention_score = attention
        self.fatigue_level   = fatigue
        self.risk_score      = risk

        # Blink counter
        if ear < Config.EAR_THRESHOLD:
            self.consec_closed += 1
        else:
            if self.consec_closed >= Config.CONSEC_FRAMES:
                self.fatigue_alerts += 1
            elif self.consec_closed > 0:
                self.blink_count += 1
            self.consec_closed = 0

        # Yawn counter
        if mar > Config.MAR_THRESHOLD:
            self.yawn_count += 1

        # Safety score deductions
        if response_level == "EMERGENCY":
            self.safety_score -= Config.PENALTY_HIGH_FATIGUE
        elif response_level == "WARNING":
            self.safety_score -= Config.PENALTY_FATIGUE_ALERT
        self.safety_score = max(0.0, self.safety_score)

        self.log.append({
            "frame":     self.frame_count,
            "ear":       round(ear, 4),
            "mar":       round(mar, 4),
            "yaw":       round(yaw, 2),
            "pitch":     round(pitch, 2),
            "roll":      round(roll, 2),
            "emotion":   emotion,
            "attention": round(attention, 2),
            "fatigue":   round(fatigue, 2),
            "risk":      round(risk, 2),
            "response":  response_level,
        })

    def to_dataframe(self):
        """Return session log as a Pandas DataFrame."""
        return pd.DataFrame(self.log)

    def summary(self):
        """Print a formatted session summary."""
        elapsed = (datetime.now() - self.session_start).seconds
        df = self.to_dataframe()
        print("=" * 55)
        print("   AURA DRIVE — Session Summary")
        print("=" * 55)
        print(f"  Duration    : {elapsed}s  ({self.frame_count} frames)")
        print(f"  Blinks      : {self.blink_count}")
        print(f"  Yawns       : {self.yawn_count}")
        print(f"  Fatigue Alerts : {self.fatigue_alerts}")
        print(f"  Avg Attention  : {df['attention'].mean():.1f}")
        print(f"  Avg Fatigue    : {df['fatigue'].mean():.1f}")
        print(f"  Avg Risk       : {df['risk'].mean():.1f}")
        print(f"  Final Safety   : {self.safety_score:.1f} / 100")
        print("=" * 55)
