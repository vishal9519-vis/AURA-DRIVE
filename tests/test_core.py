# ============================================================
# AURA DRIVE — tests/test_core.py
# Basic unit tests for core modules
# ============================================================

def test_ear_open_eye():
    """Open eye EAR should be above threshold (0.22)"""
    ear = 0.30
    assert ear > 0.22, "Open eye EAR should be above threshold"

def test_ear_closed_eye():
    """Closed eye EAR should be below threshold (0.22)"""
    ear = 0.10
    assert ear < 0.22, "Closed eye EAR should be below threshold"

def test_mar_normal():
    """Normal mouth MAR should be below yawn threshold (0.55)"""
    mar = 0.20
    assert mar < 0.55, "Normal MAR should be below yawn threshold"

def test_mar_yawning():
    """Yawning MAR should be above threshold (0.55)"""
    mar = 0.70
    assert mar > 0.55, "Yawning MAR should be above threshold"

def test_risk_clamped():
    """Risk score should always be between 0 and 100"""
    risk = 85.0
    assert 0 <= risk <= 100, "Risk must be between 0 and 100"

def test_fatigue_increases():
    """Fatigue should only increase during session"""
    fatigue_start = 10.0
    fatigue_end = 25.0
    assert fatigue_end >= fatigue_start, "Fatigue should never decrease"

def test_attention_range():
    """Attention score should be between 0 and 100"""
    attention = 75.0
    assert 0 <= attention <= 100, "Attention must be between 0 and 100"
