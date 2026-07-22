import random
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]

EMBEDDINGS = (
    ROOT /
    "test" /
    "evaluation" /
    "embeddings"
)

RESULTS = (
    ROOT /
    "test" /
    "evaluation" /
    "results"
)

RESULTS.mkdir(exist_ok=True)

persons = []

for person in EMBEDDINGS.iterdir():

    if not person.is_dir():
        continue

    files = sorted(person.glob("*.npy"))

    if len(files) >= 2:
        persons.append((person.name, files))

print(f"People with embeddings : {len(persons)}")

pairs = []

# Positive Pairs

for person, files in persons:

    for i in range(len(files)):
        for j in range(i + 1, len(files)):

            pairs.append({
                "file1": str(files[i]),
                "file2": str(files[j]),
                "label": 1
            })

print("Positive pairs :", len([p for p in pairs if p["label"] == 1]))

# Negative Pairs

negative = []

while len(negative) < len(pairs):

    p1, f1 = random.choice(persons)
    p2, f2 = random.choice(persons)

    if p1 == p2:
        continue

    negative.append({
        "file1": str(random.choice(f1)),
        "file2": str(random.choice(f2)),
        "label": 0
    })

pairs.extend(negative)

random.shuffle(pairs)

df = pd.DataFrame(pairs)

csv_path = RESULTS / "verification_pairs.csv"

df.to_csv(csv_path, index=False)

print("\nVerification pairs created")

print("Total pairs :", len(df))

print("Saved to")

print(csv_path)