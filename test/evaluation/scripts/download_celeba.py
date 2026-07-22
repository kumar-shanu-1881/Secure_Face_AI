from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]

DATASET_DIR = ROOT / "test" / "evaluation" / "dataset"
DATASET_DIR.mkdir(parents=True, exist_ok=True)

command = [
    sys.executable,
    "-m",
    "kaggle",
    "datasets",
    "download",
    "-d",
    "jessicali9530/celeba-dataset",
    "-p",
    str(DATASET_DIR),
    "--unzip"
]

print("Running command:")
print(command)

subprocess.run(command, check=True)