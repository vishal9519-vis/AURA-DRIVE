#  AURA DRIVE
## AI-Powered Adaptive Driver Intelligence & Safety System

[![GitHub](https://img.shields.io/badge/GitHub-vishal%2Faura--drive-181717?logo=github)](https://github.com/vishal/aura-drive)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green)
![dlib](https://img.shields.io/badge/dlib-19.24+-orange)
![Platform](https://img.shields.io/badge/Platform-Google%20Colab-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**Author:** vishal &nbsp;|&nbsp; **Repo:** [github.com/vishal/aura-drive](https://github.com/vishal/aura-drive)

---

##  Project Overview

AURA DRIVE is a real-time AI-powered driver monitoring and safety system built using computer vision and facial landmark analysis. It continuously monitors the driver through a webcam and detects dangerous conditions such as fatigue, drowsiness, distraction, and emotional stress — then generates intelligent adaptive safety responses.

---

##  Objectives

- Detect driver **fatigue** and **drowsiness** in real time
- Monitor **driver attention** and head direction
- Analyze **emotional state** from facial geometry
- Generate **risk predictions** and adaptive safety responses
- Provide a **live analytics dashboard** per session

---

##  Core Features

| Feature | Description |
|---------|-------------|
| **Fatigue Detection** | Tracks Eye Aspect Ratio (EAR) — alerts when eyes close too long |
| **Yawn Detection** | Tracks Mouth Aspect Ratio (MAR) — detects yawning events |
| **Head Pose Estimation** | Calculates pitch, yaw, roll — detects driver looking away |
| **Attention Score** | 0–100 score updated every frame based on all signals |
| **Fatigue Level** | Accumulates over session — never resets (like real fatigue) |
| **Emotion Detection** | Rule-based: CALM / FOCUSED / STRESSED / TIRED / YAWNING |
| **Risk Prediction** | Combines attention + fatigue + emotion into 0–100% risk |
| **Adaptive Response** | SAFE / CAUTION / WARNING / EMERGENCY messages |
| **Analytics Dashboard** | 6-chart session summary with dark-themed matplotlib |

---

##  Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Core language |
| **OpenCV** | Image processing and frame annotation |
| **dlib** | Face detection + 68-point landmark prediction |
| **scipy** | Euclidean distance calculations for EAR/MAR |
| **imutils** | Landmark index utilities |
| **NumPy** | Numerical operations |
| **Pandas** | Session log storage |
| **Matplotlib** | Analytics dashboard charts |
| **Google Colab** | Cloud runtime + webcam JS bridge |

---

##  Project Structure

```
AURA_DRIVE/
│
├── app.py                    # Main entry point
├── config.py                 # All thresholds and settings
├── requirements.txt          # Dependencies
│
├── modules/
│   ├── webcam.py             # Webcam capture (Colab JS bridge)
│   ├── face_detection.py     # dlib face detection + drawing
│   ├── eye_tracker.py        # EAR calculation + blink counting
│   ├── fatigue.py            # MAR + fatigue level tracking
│   ├── head_pose.py          # Pitch/yaw/roll + direction
│   ├── emotion.py            # Rule-based emotion detection
│   ├── risk.py               # Risk score + adaptive response
│   └── tracker.py            # Central session state manager
│
├── dashboard/
│   └── analytics.py          # 6-chart analytics dashboard
│
├── notebooks/
│   └── AURA_DRIVE_Colab.ipynb  # Full runnable Colab notebook
│
└── assets/
    ├── screenshots/ demo video 
    └── architecture.png
```

---

##  How to Run (Google Colab)

**Step 1** — Open [Google Colab](https://colab.research.google.com)

**Step 2** — Upload `notebooks/AURA_DRIVE_Colab.ipynb`

**Step 3** — Run cells in order:

| Cell | Action |
|------|--------|
| Cell 1 | Install libraries + download dlib model (~100MB) |
| Cell 2 | Load all functions (EAR, MAR, head pose, emotion, risk) |
| Cell 3 | Initialize AuraTracker session state |
| Cell 4 | Setup webcam bridge + full analyze function |
| Cell 5 | Single photo test — verify system works |
| Cell 6 | Live 10-frame session |
| Cell 7 | Generate analytics dashboard |
| Cell 8 | Full Phase 4 session (15 frames) |

>  When prompted, click **Allow** to give the browser camera access.

---

## 📊 How It Works

### EAR — Eye Aspect Ratio
```
       ||p2-p6|| + ||p3-p5||
EAR =  ──────────────────────
            2 × ||p1-p4||

Open eye  → EAR ≈ 0.25–0.35
Closed eye → EAR ≈ 0.0–0.15
Threshold  → EAR < 0.22 = alert
```

### MAR — Mouth Aspect Ratio
```
       ||v1|| + ||v2|| + ||v3||
MAR =  ──────────────────────────
              2 × ||h||

Normal → MAR ≈ 0.15
Yawning → MAR > 0.55
```

### Risk Score
```
Risk = (100 - Attention) × 0.4 + Fatigue × 0.4
     + Emotion Bonus (0/8/10/15)
     + Distraction Bonus (10)
     Clamped to 0–100
```

---

##  Dashboard Output

The analytics dashboard (Cell 7) generates a 6-chart PNG:

- EAR over time with threshold line
- MAR over time with yawn threshold
- Attention score trend
- Fatigue level curve
- Risk score per frame (color-coded bars)
- Emotion distribution pie chart

---

## Future Enhancements

- [ ] Voice alerts using gTTS
- [ ] GPS integration for location-based risk
- [ ] Cloud session storage (Google Drive)
- [ ] Mobile app alerts
- [ ] IoT sensor integration (steering wheel grip, speed)
- [ ] Deep learning emotion model (DeepFace)
- [ ] Multi-driver session comparison

---

## Development Timeline

| Day | Work Done |
|-----|-----------|
| Day 1 | Project setup, config, structure |
| Day 2 | Webcam integration, face detection |
| Day 3 | Eye tracking, EAR, MAR, head pose |
| Day 4 | Alert system, adaptive responses |
| Day 5 | Analytics dashboard, session charts |
| Day 6 | Emotion detection, risk scoring, tracker |
| Day 7 | README, architecture, screenshots |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built with  using Python, OpenCV, and dlib*
