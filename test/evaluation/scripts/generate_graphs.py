import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    auc
)

# Paths

ROOT = Path(__file__).resolve().parents[3]

RESULTS = ROOT / "test" / "evaluation" / "results"

GRAPHS = ROOT / "test" / "evaluation" / "graphs"

GRAPHS.mkdir(exist_ok=True)

# Load CSV Files

verification_file = RESULTS / "verification_results.csv"
similarity_file = RESULTS / "similarity_scores.csv"

if not verification_file.exists():
    raise FileNotFoundError(f"Missing file:\n{verification_file}")

if not similarity_file.exists():
    raise FileNotFoundError(f"Missing file:\n{similarity_file}")

verification = pd.read_csv(verification_file)
similarity = pd.read_csv(similarity_file)

# Confusion Matrix

def generate_confusion_matrix():

    print("\nGenerating Confusion Matrix...")

    cm = confusion_matrix(
        verification["true_label"],
        verification["prediction"]
    )

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=[
            "Different Person",
            "Same Person"
        ]
    )

    fig, ax = plt.subplots(figsize=(6, 6))

    disp.plot(
        cmap="Blues",
        values_format="d",
        ax=ax,
        colorbar=False
    )

    plt.title("Confusion Matrix")

    plt.tight_layout()

    plt.savefig(
        GRAPHS / "confusion_matrix.png",
        dpi=300
    )

    plt.close()

    print("✓ Saved : confusion_matrix.png")


# ROC Curve

def generate_roc_curve():

    print("\nGenerating ROC Curve...")

    fpr, tpr, thresholds = roc_curve(
        similarity["label"],
        similarity["cosine"]
    )

    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6,6))

    plt.plot(
        fpr,
        tpr,
        linewidth=2,
        label=f"AUC = {roc_auc:.4f}"
    )

    plt.plot(
        [0,1],
        [0,1],
        linestyle="--",
        color="gray"
    )

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")

    plt.title("ROC Curve")

    plt.legend(loc="lower right")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        GRAPHS / "roc_curve.png",
        dpi=300
    )

    plt.close()

    print("✓ Saved : roc_curve.png")


# Similarity Distribution

def generate_similarity_distribution():

    print("\nGenerating Similarity Distribution...")

    genuine = similarity[
        similarity["label"] == 1
    ]

    impostor = similarity[
        similarity["label"] == 0
    ]

    plt.figure(figsize=(8,5))

    plt.hist(
        impostor["cosine"],
        bins=50,
        alpha=0.6,
        label="Different Person"
    )

    plt.hist(
        genuine["cosine"],
        bins=50,
        alpha=0.6,
        label="Same Person"
    )

    plt.axvline(
        x=0.50,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Threshold = 0.50"
    )

    plt.xlabel("Cosine Similarity")
    plt.ylabel("Frequency")

    plt.title("Similarity Distribution")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        GRAPHS / "similarity_distribution.png",
        dpi=300
    )

    plt.close()

    print("✓ Saved : similarity_distribution.png")


# Main

if __name__ == "__main__":

    print("="*60)
    print("Generating Evaluation Graphs")
    print("="*60)

    generate_confusion_matrix()

    generate_roc_curve()

    generate_similarity_distribution()

    print("\n" + "="*60)
    print("All graphs generated successfully!")
    print("="*60)

    print("\nSaved in:")

    print(GRAPHS)