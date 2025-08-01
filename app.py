from flask import Flask, render_template, request, redirect, url_for, jsonify
import cv2
import face_recognition
import numpy as np
import os
import threading
from datetime import datetime

app = Flask(__name__)

known_face_encodings = []
known_face_names = []
video_threads = []
video_captures = []
stop_event = threading.Event()

FACES_DIR = 'known_faces'
os.makedirs(FACES_DIR, exist_ok=True)

def load_known_faces():
    global known_face_encodings, known_face_names
    known_face_encodings = []
    known_face_names = []
    for filename in os.listdir(FACES_DIR):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(FACES_DIR, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])


def process_camera(idx):
    cap = cv2.VideoCapture(idx)
    window_title = f"Camera {idx}"
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            if known_face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                if matches and face_distances.size > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow(window_title, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyWindow(window_title)


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/add_person', methods=['POST'])
def add_person():
    name = request.form['name'].strip()

    if not name:
        return "Name is required", 400

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Inbuilt camera only
    if not cap.isOpened():
        return "Error: Could not open camera.", 500

    count = 0
    max_images = 5
    image_delay = 1000  # milliseconds between captures

    cv2.namedWindow('Capturing Face', cv2.WINDOW_NORMAL)

    while count < max_images:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow('Capturing Face', frame)

        # Save image
        img_path = os.path.join(FACES_DIR, f"{name}_{count + 1}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"✅ Saved {img_path}")
        count += 1

        # Wait between captures (1 sec)
        cv2.waitKey(image_delay)

    cap.release()
    cv2.destroyAllWindows()

    load_known_faces()  # Update encodings
    return redirect(url_for('index'))



from flask import request
from werkzeug.utils import secure_filename

from flask import request
from werkzeug.utils import secure_filename

@app.route('/upload_face', methods=['POST'])
def upload_face():
    name = request.form.get('name', '').strip()
    image_file = request.files.get('image')

    if not name or not image_file:
        return "Missing name or image", 400

    os.makedirs(FACES_DIR, exist_ok=True)
    filename = secure_filename(image_file.filename)
    save_path = os.path.join(FACES_DIR, filename)
    image_file.save(save_path)
    print(f"✅ Saved {save_path}")

    return "OK", 200






@app.route('/start_video', methods=['POST'])
def start_video():
    stop_event.clear()
    load_known_faces()
    max_cams = 5
    for idx in range(max_cams):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            cap.release()
            thread = threading.Thread(target=process_camera, args=(idx,))
            thread.start()
            video_threads.append(thread)
    return jsonify({'status': 'started'})


@app.route('/stop_video', methods=['POST'])
def stop_video():
    stop_event.set()
    for thread in video_threads:
        thread.join()
    video_threads.clear()
    return jsonify({'status': 'stopped'})


if __name__ == '__main__':
    load_known_faces()
    app.run(debug=True)