import os
import cv2 as cv
import time
import csv
from tqdm import tqdm
import mediapipe as mp


# Initialize MediaPipe
print("Loading MediaPipe Face Detection Model...")

mp_face_detection = mp.solutions.face_detection

detector = mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

print("MediaPipe Loaded Successfully!\n")


# Dataset Folder
image_folder = "..//model selection//Humans"

if not os.path.exists(image_folder):
    raise FileNotFoundError(f"{image_folder} folder not found.")

image_files = [
    f for f in os.listdir(image_folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

print(f"Found {len(image_files)} images.\n")


# CSV Output
csv_file = "MediaPipe_Evaluation_Results.csv"

total_faces = 0
total_latency = 0

with open(csv_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Image Name",
        "Faces Detected",
        "Latency (ms)"
    ])

    for img_name in tqdm(image_files):

        img_path = os.path.join(image_folder, img_name)

        img = cv.imread(img_path)

        if img is None:
            continue

        rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        start = time.perf_counter()

        results = detector.process(rgb)

        latency = (time.perf_counter() - start) * 1000

        face_count = (
            len(results.detections) if results.detections else 0 )

        writer.writerow([
            img_name,
            face_count,
            round(latency, 2)
        ])

        total_faces += face_count
        total_latency += latency

avg_latency = total_latency / len(image_files)

print("\n========== BENCHMARK SUMMARY ==========")
print("Model            : MediaPipe")
print(f"Images Processed : {len(image_files)}")
print(f"Total Faces      : {total_faces}")
print(f"Average Latency  : {avg_latency:.2f} ms")
print(f"CSV File Saved   : {csv_file}")
print("=======================================")