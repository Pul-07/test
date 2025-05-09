pkg install openssh python -y
pip install flask

# Crée un mini serveur Flask qui stream la caméra
cat > server.py <<EOF
from flask import Flask, Response
import cv2

app = Flask(__name__)

def gen():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port=8080)
EOF

# Démarre le serveur
python server.py
