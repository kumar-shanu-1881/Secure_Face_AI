import sys
from pathlib import Path
import cv2 as cv

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from app.core.face_detector import Detect_face

DATASET = (
    ROOT /
    "test" /
    "evaluation" /
    "dataset" /
    "celeba_subset"
)

image_path = next(DATASET.glob("*.jpg"))

print("Image:", image_path)
import numpy as np

image = cv.imdecode(
    np.fromfile(str(image_path), dtype=np.uint8),
    cv.IMREAD_COLOR
)
print("Image Loaded:", image is not None)

detector = Detect_face()

print("Calling detector...")

result = detector.detect(image)

print(result)