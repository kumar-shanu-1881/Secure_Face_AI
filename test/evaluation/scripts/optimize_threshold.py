from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


ROOT = Path(__file__).resolve().parents[3]

CSV = (
    ROOT /
    "test" /
    "evaluation" /
    "results" /
    "similarity_scores.csv"
)

RESULTS = (
    ROOT /
    "test" /
    "evaluation" /
    "results"
)


df = pd.read_csv(CSV)

print("=" * 60)
print("Optimizing Thresholds")
print("=" * 60)
print(f"Pairs : {len(df)}")


results = []

cosine_thresholds = np.arange(0.50, 0.91, 0.02)

euclidean_thresholds = np.arange(0.80, 1.31, 0.05)


for cos_t in cosine_thresholds:

    for euc_t in euclidean_thresholds:

        prediction = (
            (df["cosine"] >= cos_t)
            &
            (df["euclidean"] <= euc_t)
        ).astype(int)

        accuracy = accuracy_score(df["label"], prediction)

        precision = precision_score(
            df["label"],
            prediction,
            zero_division=0
        )

        recall = recall_score(
            df["label"],
            prediction,
            zero_division=0
        )

        f1 = f1_score(
            df["label"],
            prediction,
            zero_division=0
        )

        results.append({

            "Cosine": round(cos_t,2),

            "Euclidean": round(euc_t,2),

            "Accuracy": accuracy,

            "Precision": precision,

            "Recall": recall,

            "F1": f1

        })


result_df = pd.DataFrame(results)

result_df = result_df.sort_values(
    by="F1",
    ascending=False
)

csv_path = RESULTS / "threshold_results.csv"

result_df.to_csv(csv_path, index=False)

print("\nTop 10 Thresholds\n")

print(result_df.head(10))

print("\nSaved to")

print(csv_path)