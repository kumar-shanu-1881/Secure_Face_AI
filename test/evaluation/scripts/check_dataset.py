from pathlib import Path


BASE = Path(__file__).resolve().parent.parent

LFW = BASE / "dataset" / "lfw" / "lfw_funneled"
WIDER = BASE / "dataset" / "widerface"
CELEBA = BASE / "dataset" / "celeba"

CELEBA_IMAGES = CELEBA / "img_align_celeba"

ATTR = CELEBA / "list_attr_celeba.csv"
BBOX = CELEBA / "list_bbox_celeba.csv"
LANDMARK = CELEBA / "list_landmarks_align_celeba.csv"
PARTITION = CELEBA / "list_eval_partition.csv"

print("=" * 60)
print("Checking Evaluation Datasets...\n")

# LWF

if LFW.exists():

    persons = [folder for folder in LFW.iterdir() if folder.is_dir()]
    images = list(LFW.rglob("*.jpg"))

    print("✓ LFW Dataset Found")
    print(f"Persons : {len(persons)}")
    print(f"Images  : {len(images)}")

else:

    print("✗ LFW Dataset NOT FOUND")

print()

# WIDER FACE

if WIDER.exists():

    images = list(WIDER.rglob("*.jpg"))

    print("✓ WIDER FACE Dataset Found")
    print(f"Images : {len(images)}")

else:

    print("✗ WIDER FACE Dataset NOT FOUND")

print()

# CELEBA

if CELEBA.exists():

    print("✓ CelebA Dataset Found")

    if CELEBA_IMAGES.exists():

        images = list(CELEBA_IMAGES.glob("*.jpg"))

        print(f"Images : {len(images)}")

    else:

        print("✗ img_align_celeba folder missing")

    print()

    print(
        f"Attributes File     : {'✓ Found' if ATTR.exists() else '✗ Missing'}"
    )

    print(
        f"Bounding Box File   : {'✓ Found' if BBOX.exists() else '✗ Missing'}"
    )

    print(
        f"Landmark File       : {'✓ Found' if LANDMARK.exists() else '✗ Missing'}"
    )

    print(
        f"Partition File      : {'✓ Found' if PARTITION.exists() else '✗ Missing'}"
    )

    if CELEBA_IMAGES.exists():

        print("\nFirst Five Images:")

        for img in sorted(CELEBA_IMAGES.glob("*.jpg"))[:5]:
            print(img.name)

else:

    print("✗ CelebA Dataset NOT FOUND")

print("\n" + "=" * 60)