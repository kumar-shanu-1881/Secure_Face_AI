import sys
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

# Project Root

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

# Verification Pair File

PAIR_FILE = (
    ROOT /
    "test" /
    "evaluation" /
    "results" /
    "verification_pairs.csv"
)

RESULTS = (
    ROOT /
    "test" /
    "evaluation" /
    "results"
)

RESULTS.mkdir(exist_ok=True)


pairs = pd.read_csv(PAIR_FILE)

print("=" * 60)
print("Computing Similarity Scores")
print("=" * 60)
print(f"Verification Pairs : {len(pairs)}")

# Cache embeddings (avoid loading same file repeatedly)

cache = {}

rows = []

for _, row in tqdm(pairs.iterrows(), total=len(pairs)):

    file1 = row["file1"]
    file2 = row["file2"]

    if file1 not in cache:
        cache[file1] = np.load(file1)

    if file2 not in cache:
        cache[file2] = np.load(file2)

    emb1 = cache[file1]
    emb2 = cache[file2]

    # Cosine Similarity
    cosine = np.dot(emb1, emb2)

    # Euclidean Distance
    euclidean = np.linalg.norm(emb1 - emb2)

    rows.append(
        {
            "file1": file1,
            "file2": file2,
            "label": int(row["label"]),
            "cosine": float(cosine),
            "euclidean": float(euclidean)
        }
    )


df = pd.DataFrame(rows)

csv_path = RESULTS / "similarity_scores.csv"

df.to_csv(csv_path, index=False)

print("\n" + "=" * 60)
print("Similarity Computation Finished")
print("=" * 60)

print(f"Pairs Processed : {len(df)}")
print(f"Saved To : {csv_path}")