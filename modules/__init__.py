# AURA DRIVE — modules package
# Using try/except so each module can be imported independently if needed

try:
    from modules.webcam         import take_photo_js, resize_frame
    from modules.face_detection import load_predictor, detect_faces, get_landmarks
    from modules.eye_tracker    import get_ear, draw_eyes
    from modules.fatigue        import get_mar, update_fatigue
    from modules.head_pose      import estimate_head_pose, is_distracted
    from modules.emotion        import detect_emotion
    from modules.risk           import compute_risk, adaptive_response, update_attention
    from modules.tracker        import AuraTracker
except ImportError:
    pass  # Allow individual module imports without full package
