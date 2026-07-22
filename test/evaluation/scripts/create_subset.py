from pathlib import Path
import random
import shutil

BASE = Path(__file__).resolve().parent.parent

SOURCE = (
    BASE /
    "dataset" /
    "celeba" /
    "img_align_celeba"
)

destination = (
    BASE /
    "dataset" /
    "celeba_subset"
)


num_of_images = 10000

random.seed(42)

destination.mkdir(exist_ok=True)

images = list(SOURCE.glob("*.jpg"))

print(f"Total Images Found : {len(images)}")

selected = random.sample(images, num_of_images)

print(f"Copying {num_of_images} images...\n")

for image in selected:

    shutil.copy2(
        image,
        destination / image.name
    )

print("========================================")

print("Subset Created Successfully")

print(f"Saved At : {destination}")

print(f"Images   : {len(list(destination.glob('*.jpg')))}")

