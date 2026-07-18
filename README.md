# 🔐 SecureFace AI

A real-time **Face Authentication System** built using **Flask**, **MediaPipe**, **InsightFace (ArcFace)**, and **MongoDB**. SecureFace AI authenticates users using both traditional credentials and biometric facial recognition for enhanced security.

---

## 📌 Features

- 👤 User Registration
- 🔑 Secure Login using Face + Password
- 📷 Real-Time Webcam Face Capture
- 😊 Face Detection using MediaPipe
- 🧠 Face Recognition using InsightFace (ArcFace)
- 📐 512-D Face Embeddings
- 📊 Cosine Similarity & Euclidean Distance Matching
- 🔒 Password Hashing (Werkzeug - Scrypt)
- 💾 MongoDB Database Integration
- 🆔 Automatic User ID Generation
- ⏳ Session-based Authentication (2 Days)
- 📱 Responsive User Interface
- 🧪 Face Similarity Testing Module

---

# 🚀 Demo

### Landing Page

- Project Introduction
- Features Overview
- Login/Register Navigation

### Registration

- User Details
- Live Face Capture
- Face Embedding Generation
- Secure Password Storage

### Login

- User ID Verification
- Email Verification
- Password Verification
- Live Face Verification
- Dashboard Access

### Dashboard

- User Profile
- Project Information
- Authentication Status
- Technology Stack

---

# 🏗 Project Architecture

```
SecureFace AI
│
├── app
│   │
│   ├── api
│   │   ├── detect.py
│   │   ├── register.py
│   │   ├── login.py
│   │   └── dashboard.py
│   │
│   ├── core
│   │   ├── face_detector.py
│   │   ├── get_embedings.py
│   │   ├── check_similarity.py
│   │   └── anti_spoof.py (Future)
│   │
│   ├── db
│   │   ├── mongodb.py
│   │   └── user_repo.py
│   │
│   └── __init__.py
│
├── image
├── static
├── templates
├── test
│
├── .env
├── requirements.txt
├── run.py
└── README.md
```

---

# ⚙️ Technology Stack

## Backend

- Python
- Flask
- REST API

## Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API

## Computer Vision

- OpenCV
- MediaPipe

## Face Recognition

- InsightFace
- ArcFace (buffalo_sc)

## Machine Learning

- NumPy

## Database

- MongoDB Atlas

## Security

- Werkzeug Security (Scrypt)
- Flask Sessions
- Environment Variables

---

# 🧠 AI Pipeline

## Registration Flow

```
User
      │
      ▼
Capture Face
      │
      ▼
MediaPipe Face Detection
      │
      ▼
Face Crop
      │
      ▼
InsightFace Embedding
      │
      ▼
Generate User ID
      │
      ▼
Hash Password
      │
      ▼
Store User Data
      │
      ▼
MongoDB
```

---

## Login Flow

```
User
      │
      ▼
Capture Live Face
      │
      ▼
MediaPipe Detection
      │
      ▼
Generate Face Embedding
      │
      ▼
Verify Email
      │
      ▼
Verify User ID
      │
      ▼
Verify Password
      │
      ▼
Compare Face Embeddings
      │
      ▼
Authentication Success
      │
      ▼
Dashboard
```

---

# 🔍 Face Recognition Pipeline

```
Input Image
      │
      ▼
MediaPipe Face Detection
      │
      ▼
Face Crop
      │
      ▼
InsightFace ArcFace
      │
      ▼
512-D Face Embedding
      │
      ▼
Cosine Similarity
      │
      ▼
Euclidean Distance
      │
      ▼
Authentication Result
```

---

# 📊 Face Matching

The system compares two facial embeddings using:

- Cosine Similarity
- Euclidean Distance

Authentication is successful only if both similarity metrics satisfy predefined thresholds.

---

# 🔒 Security Features

- Password Hashing using Scrypt
- Session Authentication
- Environment Variables
- Face Authentication
- User ID Validation
- Email Validation

---

# 📂 Database Schema

Each registered user contains:

| Field | Description |
|--------|-------------|
| User ID | Unique Generated ID |
| Name | User Name |
| Email | User Email |
| Password | Hashed Password |
| Face Embedding | 512-D Vector |
| Created At | Registration Date |

---

# 🧪 Testing

The project includes testing modules for:

### Face Detection

- Detect face successfully
- Face crop validation

### Face Embedding

- Generate 512-dimensional embeddings

### Similarity Testing

Tests include:

- Same Person Matching
- Different Person Matching

Outputs:

- Cosine Similarity
- Euclidean Distance
- Match Decision

Results are stored in:

```
similarity_results.csv
```

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/SecureFace-AI.git

cd SecureFace-AI
```

---

## Create Virtual Environment

```bash
python -m venv faceenv
```

Activate

Windows

```bash
faceenv\Scripts\activate
```

Linux/Mac

```bash
source faceenv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file

```env
MONGO_URI=your_mongodb_connection_string

SECRET_KEY=your_secret_key
```

---

## Run Project

```bash
python run.py
```

Application will run at

```
http://127.0.0.1:10000
```

---

# 📈 Future Improvements

- Anti-Spoof Detection (MiniFASNet)
- JWT Authentication
- PostgreSQL Support
- Qdrant Vector Database
- Docker Deployment
- Redis Session Storage
- Admin Dashboard
- Authentication Logs
- Email Verification
- Password Reset
- Face Registration History
- Multi-Factor Authentication

---

# 🎯 Project Highlights

- Real-Time Face Authentication
- Secure User Registration
- Face + Password Login
- InsightFace ArcFace Recognition
- MediaPipe Face Detection
- MongoDB Integration
- Flask Modular Architecture
- Session-Based Authentication
- Face Similarity Evaluation
- Production-Oriented Design

---

# 👨‍💻 Author

**Kumar Shanu**

B.Tech Computer Science Engineering (AI & ML)

Machine Learning & Full Stack Developer

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!