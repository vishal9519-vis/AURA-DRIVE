# ============================================================
#  AURA DRIVE — modules/webcam.py
#  Webcam capture using Google Colab JS bridge
# ============================================================

try:
    from IPython.display import display, Javascript
    from google.colab.output import eval_js
    COLAB = True
except ImportError:
    COLAB = False

from base64 import b64decode
import numpy as np
import cv2
from config import Config


def take_photo_js():
    """JavaScript bridge to capture a webcam frame in Google Colab."""
    js = Javascript("""
        async function takePhoto(quality) {
            const div = document.createElement('div');
            const video = document.createElement('video');
            video.style.display = 'block';
            const stream = await navigator.mediaDevices.getUserMedia({video: true});
            document.body.appendChild(div);
            div.appendChild(video);
            video.srcObject = stream;
            await video.play();
            google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);
            await new Promise((resolve) => setTimeout(resolve, 500));
            const canvas = document.createElement('canvas');
            canvas.width  = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            stream.getVideoTracks()[0].stop();
            div.remove();
            return canvas.toDataURL('image/jpeg', quality);
        }
    """)
    display(js)
    data = eval_js(f"takePhoto({Config.WEBCAM_QUALITY})")
    binary = b64decode(data.split(',')[1])
    arr = np.frombuffer(binary, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return frame


def get_local_webcam():
    """Open webcam on local laptop / VS Code."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")
    return cap


def resize_frame(frame):
    """Resize frame to configured dimensions."""
    return cv2.resize(frame, (Config.WEBCAM_WIDTH, Config.WEBCAM_HEIGHT))
