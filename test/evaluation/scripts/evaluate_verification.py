import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
)
from tqdm import tqdm
# Project Root
ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))
# Import Your Similarity Module
from app.core.check_similarity import compare_faces

# Paths

PAIR_CSV = (
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

# Load Verification Pairs

df = pd.read_csv(PAIR_CSV)

print("=" * 60)
print("SecureFace AI Verification Evaluation")
print("=" * 60)
print(f"Verification Pairs : {len(df)}")
print()

# Evaluation

y_true = []
y_pred = []

cosine_scores = []
euclidean_scores = []

rows = []

for _, row in tqdm(df.iterrows(), total=len(df)):

    emb1 = np.load(row["file1"])
    emb2 = np.load(row["file2"])

    matched, cosine, euclidean = compare_faces(emb1, emb2)

    y_true.append(int(row["label"]))
    y_pred.append(int(matched))

    cosine_scores.append(cosine)
    euclidean_scores.append(euclidean)

    rows.append(
        {
            "file1": Path(row["file1"]).name,
            "file2": Path(row["file2"]).name,
            "true_label": int(row["label"]),
            "prediction": int(matched),
            "cosine_similarity": round(float(cosine), 6),
            "euclidean_distance": round(float(euclidean), 6),
        }
    )

# Metrics

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

auc = roc_auc_score(y_true, cosine_scores)

cm = confusion_matrix(y_true, y_pred)

tn, fp, fn, tp = cm.ravel()

far = fp / (fp + tn)
frr = fn / (fn + tp)

# Print Results

print("\n" + "=" * 60)

print("Verification Results\n")

print(f"Accuracy              : {accuracy*100:.2f}%")
print(f"Precision             : {precision*100:.2f}%")
print(f"Recall                : {recall*100:.2f}%")
print(f"F1 Score              : {f1*100:.2f}%")
print(f"ROC-AUC               : {auc:.4f}")

print()

print(f"False Acceptance Rate : {far*100:.2f}%")
print(f"False Rejection Rate  : {frr*100:.2f}%")

print()

print("Confusion Matrix")
print(cm)

print()

print(f"True Positive  : {tp}")
print(f"True Negative  : {tn}")
print(f"False Positive : {fp}")
print(f"False Negative : {fn}")

print("=" * 60)

# Save Detailed Results

result_df = pd.DataFrame(rows)

csv_path = RESULTS / "verification_results.csv"

result_df.to_csv(csv_path, index=False)

print("\nDetailed results saved to:")
print(csv_path)