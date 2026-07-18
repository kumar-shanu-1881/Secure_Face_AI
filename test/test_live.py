import cv2

from app.core.get_embedings import get_embedder
from app.core.check_similarity import compare_faces

embedder = get_embedder

cap = cv2.VideoCapture(0)

embedding1 = None
embedding2 = None

capture_count = 0

print("=" * 50)
print("SPACE -> Capture Image")
print("Capture 2 images")
print("ESC -> Finish and Compare")
print("=" * 50)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    display = frame.copy()

    if capture_count == 0:
        cv2.putText(
            display,
            "Press SPACE to capture Image 1",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

    elif capture_count == 1:
        cv2.putText(
            display,
            "Press SPACE to capture Image 2",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )

    else:
        cv2.putText(
            display,
            "Press ESC to Compare",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2,
        )

    cv2.imshow("SecureFace AI Test", display)

    key = cv2.waitKey(1) & 0xFF

    # SPACE pressed
    if key == 32:

        embedding = embedder.get_embedding(frame)

        if embedding is None:
            print("No face detected. Try again.")
            continue

        if capture_count == 0:
            embedding1 = embedding
            capture_count = 1
            print("Image 1 captured.")

        elif capture_count == 1:
            embedding2 = embedding
            capture_count = 2
            print("Image 2 captured.")

        else:
            print("Already captured both images.")

    # ESC pressed
    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()


print("\nComparing Faces...\n")

if embedding1 is None:
    print("Image 1 not captured.")

elif embedding2 is None:
    print("Image 2 not captured.")

else:

    matched, cosine, euclidean = compare_faces(
        embedding1,
        embedding2
    )

    print("=" * 50)
    print("RESULT")
    print("=" * 50)
    print(f"Matched            : {matched}")
    print(f"Cosine Similarity  : {cosine:.4f}")
    print(f"Euclidean Distance : {euclidean:.4f}")
    print("=" * 50)