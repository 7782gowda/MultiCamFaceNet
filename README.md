

````markdown
# 👤 MultiCamFaceNet

**MultiCamFaceNet** is a real-time multi-camera face recognition system built with **Flask**, **OpenCV**, and **face_recognition**. It allows you to add people via a webcam, recognize them using up to 5 cameras, and control everything via a browser-based dashboard.

---

## 📸 Features

- ➕ Add a new person using the **inbuilt webcam**
- 🖼 Upload face images from the browser
- 🎥 Start/Stop video capture from up to **5 cameras**
- 🧠 Real-time face recognition with name overlay
- 🗂 Stores each person with **5 captured images**
- 🔁 Automatically updates known faces when added
- ⚙️ Runs face matching on reduced resolution for better performance

---

## 🧠 Tech Stack

| Technology        | Description                    |
|------------------|--------------------------------|
| Python 3.x        | Core backend language          |
| Flask             | Web backend framework          |
| OpenCV            | Camera input and display       |
| face_recognition  | Face detection and encoding    |
| HTML + JS         | Web interface and controls     |

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/7782gowda/MultiCamFaceNet.git
cd MultiCamFaceNet
````

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

> If you face issues with `face_recognition`, try:

```bash
pip install cmake
pip install dlib
pip install face_recognition
```

### 3. Run the App

```bash
python app.py
```

Open your browser and visit:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Usage Guide

### ➕ Add Person

* Click **"Add Person"**
* Enter a name and submit
* Your inbuilt webcam captures **5 face images**
* Camera closes automatically

### 📤 Upload via Browser

* Use the form to upload a `.jpg` or `.png` image
* Add a label (name), and the app will encode it

### 🎥 Start Video Recognition

* Click **"Start Video"**
* Up to 5 camera windows pop up, one for each device
* If faces match known images, names are displayed

### 🛑 Stop Video Recognition

* Click **"Stop Video"** to terminate all live captures

---

## 📁 Project Structure

```
MultiCamFaceNet/
├── app.py                  # Main backend app
├── templates/
│   └── dashboard.html      # Web UI dashboard
├── known_faces/            # Stores captured face images
├── static/                 # (optional) For future CSS/JS
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuration Tips

You can change the number of cameras and resolution in `app.py`:

```python
max_cams = 5  # Max camera devices to scan

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
```

Lower resolution = faster recognition.

---

## 📌 To Do / Ideas

* [ ] Stream live video feed into the browser (WebRTC)
* [ ] Export face recognition logs to CSV
* [ ] Admin login to manage face records
* [ ] Add face match confidence threshold settings

---

## 👨‍💻 Developed By

**Suprith M S**
M.Tech in Computer Science
Siddaganga Institute of Technology
[GitHub: @7782gowda](https://github.com/7782gowda)

---

> 📂 This project is for educational and demonstration purposes. Use responsibly.

```

