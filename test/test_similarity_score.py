import os
import cv2
import csv
from app.core.get_embedings import get_embedder
from app.core.check_similarity import compare_faces

embedder = get_embedder 

# Folder path where your dataset resides
DATASET = "images/Celebrity Faces Dataset" 

def get_embedding(image_path):
    frame = cv2.imread(image_path)
    
    if frame is None:
        print(f"Cannot read image file: {image_path}")
        return None

    # Let your custom get_embedder handle detection and extraction directly from the raw frame
    try:
        embedding = embedder.get_embedding(frame)
        
        # Guard against your module returning None if it fails to find a face internally
        if embedding is None:
            print(f"Embedding extraction returned None (No face found by model): {image_path}")
            return None
            
        return embedding
    except Exception as e:
        print(f"Model failed processing image {image_path}: {e}")
        return None


csv_file = open("similarity_results.csv", "w", newline="")
writer = csv.writer(csv_file)
writer.writerow([
    "Person1", "Image1", "Person2", "Image2", 
    "Cosine Similarity", "Euclidean Distance", "Predicted", "Actual"
])

# Filter out hidden files and read valid directories
persons = sorted([d for d in os.listdir(DATASET) if os.path.isdir(os.path.join(DATASET, d))])


print("\n========== SAME PERSON ==========\n")

for person in persons:
    folder = os.path.join(DATASET, person)
    images = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    for i in range(len(images)):
        for j in range(i + 1, len(images)):
            img1 = os.path.join(folder, images[i])
            img2 = os.path.join(folder, images[j])

            emb1 = get_embedding(img1)
            emb2 = get_embedding(img2)

            if emb1 is None or emb2 is None:
                continue

            matched, cosine, euclidean = compare_faces(emb1, emb2)

            print(f"{person} : {images[i]} vs {images[j]} -> Cos={cosine:.4f} Dist={euclidean:.4f} Match={matched}")
            
            writer.writerow([
                person, images[i], person, images[j], 
                cosine, euclidean, matched, "Same"
            ])


# ==========================================================
# DIFFERENT PERSON TEST
# ==========================================================

print("\n========== DIFFERENT PERSON ==========\n")

for i in range(len(persons)):
    for j in range(i + 1, len(persons)):
        person1 = persons[i]
        person2 = persons[j]
        
        folder1 = os.path.join(DATASET, person1)
        folder2 = os.path.join(DATASET, person2)
        
        images_p1 = sorted([f for f in os.listdir(folder1) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        images_p2 = sorted([f for f in os.listdir(folder2) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

        if not images_p1 or not images_p2:
            continue
            
        img1_name = images_p1[0]
        img2_name = images_p2[0]

        img1 = os.path.join(folder1, img1_name)
        img2 = os.path.join(folder2, img2_name)

        emb1 = get_embedding(img1)
        emb2 = get_embedding(img2)

        if emb1 is None or emb2 is None:
            continue

        matched, cosine, euclidean = compare_faces(emb1, emb2)

        print(f"{person1} vs {person2} -> Cos={cosine:.4f} Dist={euclidean:.4f} Match={matched}")

        writer.writerow([
            person1, img1_name, person2, img2_name, 
            cosine, euclidean, matched, "Different"
        ])


csv_file.close()

print("\n===================================")
print("Testing Completed")
print("Results saved to similarity_results.csv")
print("===================================")


# python -m test.test_similarity_score this run in bash to run this file 