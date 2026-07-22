import sys
import gc
from pathlib import Path

import cv2 as cv
import numpy as np
from tqdm import tqdm

# Project Root

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

# Import your existing models

from app.core.face_detector import Detect_face
from app.core.get_embedings import get_embedder

# Dataset

LFW = (
    ROOT /
    "test" /
    "evaluation" /
    "dataset" /
    "lfw" /
    "lfw_funneled"
)

OUTPUT = (
    ROOT /
    "test" /
    "evaluation" /
    "embeddings"
)

OUTPUT.mkdir(exist_ok=True)


detector = Detect_face()

persons = [p for p in LFW.iterdir() if p.is_dir()]

print("=" * 60)
print(f"People : {len(persons)}")
print("=" * 60)

success = 0
failed = 0


for person in tqdm(persons):

    person_output = OUTPUT / person.name
    person_output.mkdir(exist_ok=True)

    images = sorted(person.glob("*.jpg"))

    for img_path in images:

        image = cv.imdecode(
            np.fromfile(str(img_path), dtype=np.uint8),
            cv.IMREAD_COLOR
        )

        if image is None:
            failed += 1
            continue

        result = detector.detect(image)

        if not result["success"]:
            failed += 1
            continue

        embedding = get_embedder.get_embedding(result["face"])

        if embedding is None:
            failed += 1
            continue

        save_path = person_output / f"{img_path.stem}.npy"

        np.save(save_path, embedding)

        success += 1

        del image
        del embedding
        gc.collect()


print("\n" + "=" * 60)
print("Embedding Generation Completed")
print("=" * 60)

print(f"Successful : {success}")
print(f"Failed     : {failed}")

print(f"\nSaved to:\n{OUTPUT}")