import cv2
import sys
import numpy as np

# Import your core modules exactly as they are in the project
from app.core.face_detector import Detect_face
from app.core.get_embedings import get_embedder

def run_diagnostics(image_path):
    print(f"\n[{image_path}] STARTING PIPELINE DIAGNOSTICS...")
    print("-" * 50)

    # 1. Load the Image
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"❌ ERROR: Could not find or read the image at '{image_path}'.")
        print("Please check the file name and path.")
        return

    print("✔ [1/3] Image loaded into memory successfully.")

    # 2. Run the Face Detector
    detector = Detect_face()
    detect_result = detector.detect(frame)

    if not detect_result["success"]:
        print("\n❌ DETECTOR FAILED:")
        print(f"Reason: {detect_result.get('message', 'Unknown error')}")
        return

    print("✔ [2/3] Face Detector passed.")
    print(f"    - Bounding Box Found: {detect_result['bbox']}")
    print(f"    - Message: {detect_result['message']}")

    # 3. Run the Embedder
    # Passing the full original frame exactly like we did in the final fix!
    embedder = get_embedder 
    embedding = embedder.get_embedding(frame)

    if embedding is None:
        print("\n❌ EMBEDDER FAILED:")
        print("Reason: The model returned 'None'. The image might be too low quality, heavily cropped, or severely poorly lit.")
        return

    print("✔ [3/3] Face Embedder passed.")
    print(f"    - Output Type: {type(embedding)}")
    print(f"    - Vector Shape: {np.array(embedding).shape}")
    
    # Print the first 5 numbers of the embedding array to prove it worked
    sample_values = np.round(embedding[:5], 4).tolist()
    print(f"    - Sample Data: {sample_values} ...")

    print("-" * 50)
    print("🎉 SUCCESS! BOTH MODELS ARE WORKING PERFECTLY.")
    print("-" * 50)


if __name__ == "__main__":
    # If you run: python test_pipeline.py my_face.jpg
    if len(sys.argv) > 1:
        target_image = sys.argv[1]
    else:
        # If you just run: python test_pipeline.py
        target_image = input("Enter the file name of your test image (e.g., test.jpg): ")
    
    run_diagnostics(target_image)