import sys
import time
from pathlib import Path
import numpy as np
import cv2 as cv
import pandas as pd
from tqdm import tqdm

# Add Project Root
ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))
# Import Detector
from app.core.face_detector import Detect_face

# Dataset

DATASET = (
    ROOT /
    "test" /
    "evaluation" /
    "dataset" /
    "celeba_subset"
)

RESULTS = (
    ROOT /
    "test" /
    "evaluation" /
    "results"
)

RESULTS.mkdir(exist_ok=True)


detector = Detect_face()

image_paths = sorted(DATASET.glob("*.jpg"))


print("=" * 60)
print(f"Dataset Path : {DATASET}")
print(f"Images Found : {len(image_paths)}")
print("=" * 60)

successful = 0
failed = 0

no_face = 0
multiple_faces = 0
not_forward = 0
other = 0

times = []
rows = []


for img_path in tqdm(image_paths):
    try:
        image = cv.imdecode(
            np.fromfile(str(img_path), dtype=np.uint8),
            cv.IMREAD_COLOR
        )
    except Exception as e:
        print(f"Cannot read image: {img_path}")
        print(e)
        continue

    if image is None:
        print(f"Cannot decode image: {img_path}")
        continue

    try:

        start = time.perf_counter()

        result = detector.detect(image)

        end = time.perf_counter()

        elapsed = end - start

        times.append(elapsed)

        if result["success"]:

            successful += 1

        else:

            failed += 1

            msg = result["message"]

            if msg == "No face detected.":
                no_face += 1

            elif msg == "Multiple faces detected.":
                multiple_faces += 1

            elif msg == "Please look straight at the camera.":
                not_forward += 1

            else:
                other += 1

        rows.append(
            {
                "image": img_path.name,
                "success": result["success"],
                "message": result["message"],
                "time_ms": round(elapsed * 1000, 2)
            }
        )

    except Exception as e:

        print(f"\nERROR processing {img_path.name}")
        print(e)

        failed += 1


print("\nFinished Processing")

print(f"Successful : {successful}")
print(f"Failed     : {failed}")
print(f"Times Count: {len(times)}")

if len(times) == 0:
    print("\nNo images were successfully processed.")
    print("Stopping evaluation.")
    exit()

accuracy = successful / (successful + failed)

avg_time = sum(times) / len(times)

fps = 1 / avg_time


print("\n" + "=" * 60)

print("SecureFace AI Detection Evaluation\n")

print(f"Images Processed      : {successful + failed}")
print(f"Successful            : {successful}")
print(f"Failed                : {failed}")

print()

print(f"Validation Accuracy   : {accuracy*100:.2f}%")

print()

print(f"Average Time          : {avg_time*1000:.2f} ms")
print(f"FPS                   : {fps:.2f}")

print()

print("Failure Analysis")

print("------------------------------")

print(f"No Face              : {no_face}")
print(f"Multiple Faces       : {multiple_faces}")
print(f"Not Looking Straight : {not_forward}")
print(f"Other                : {other}")

print("=" * 60)

df = pd.DataFrame(rows)

csv_path = RESULTS / "validation_results.csv"

df.to_csv(csv_path, index=False)

print("\nResults saved to")

print(csv_path)