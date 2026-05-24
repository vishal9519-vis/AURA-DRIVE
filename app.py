# ============================================================
# AURA DRIVE — app.py
# AI-Powered Adaptive Driver Intelligence & Safety System
# Entry point — run this file to start the system
#
# Author: AURA DRIVE Team
# Version: 1.0.0
# ============================================================

from config import Config
from modules.tracker import AuraTracker
from modules.webcam import capture_frame
from modules.face_detection import detect_face
from modules.eye_tracker import get_ear
from modules.fatigue import get_mar, update_fatigue
from modules.head_pose import get_head_pose
from modules.emotion import detect_emotion
from modules.risk import compute_risk

def main():
    print("=" * 55)
    print("  AURA DRIVE — AI Driver Safety System")
    print("  Version:", Config.VERSION)
    print("=" * 55)
    print("  Initializing modules...")

    tracker = AuraTracker()

    print("  Status : Ready")
    print("=" * 55)

    for frame_num in range(1, 16):  # 15 frame session
        print(f"\n[Frame {frame_num}] Capturing...")

        frame = capture_frame()
        if frame is None:
            print("  No frame captured. Skipping.")
            continue

        face, landmarks = detect_face(frame)
        if landmarks is None:
            print("  No face detected.")
            continue

        # Core signals
        ear = get_ear(landmarks)
        mar, mouth = get_mar(landmarks)
        pitch, yaw, roll, direction = get_head_pose(landmarks, frame)
        is_distracted = direction != "FORWARD"
        emotion = detect_emotion(ear, mar, is_distracted)

        # Update session state
        tracker.update(ear, mar, emotion, is_distracted)

        # Risk
        risk, response = compute_risk(
            tracker.attention_score,
            tracker.fatigue_level,
            emotion,
            is_distracted
        )

        # Print live summary
        print(f"  EAR: {ear:.3f} | MAR: {mar:.3f} | Direction: {direction}")
        print(f"  Emotion: {emotion} | Attention: {tracker.attention_score:.1f}")
        print(f"  Fatigue: {tracker.fatigue_level:.1f} | Risk: {risk:.1f}%")
        print(f"  Response: {response}")

    print("\n" + "=" * 55)
    print("  Session complete. Generating dashboard...")
    print("=" * 55)
    tracker.save_log()

if __name__ == "__main__":
    main()
