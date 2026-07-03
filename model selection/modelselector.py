import os
import pandas as pd


class ModelSelector:

    def __init__(self):
        self.models = ["MTCNN", "MediaPipe", "RetinaFace"]
        self.results = {}

    def get_file_path(self, model):
        return rf"C:\Users\bnsah\OneDrive\文档\PROJECTS(FINAL)\SecureFace AI\model selection\{model}_Evaluation_Results.csv"

    def show_sample_results(self, model):

        file_name = self.get_file_path(model)

        if not os.path.exists(file_name):
            print(f"\n{model} CSV file not found.\n")
            return

        # Read CSV (Original data remains unchanged)
        df = pd.read_csv(file_name)

        # Work on a copy
        sample_df = df.copy()

        # Create temporary Status column
        sample_df["Status"] = sample_df["Faces Detected"].apply(
            lambda x: "Success" if x > 0 else "Failure"
        )

        print("\n" + "=" * 90)
        print(f"{model.upper()} SAMPLE RESULTS (First 5 Rows)")
        print("=" * 90)

        print(
            sample_df[
                [
                    "Image Name",
                    "Faces Detected",
                    "Latency (ms)",
                    "Status",
                ]
            ]
            .head()
            .to_string(index=False)
        )

    def read_results(self, model):

        file_name = self.get_file_path(model)

        if not os.path.exists(file_name):
            return None

        # Read CSV
        df = pd.read_csv(file_name)

        # Work on a copy
        working_df = df.copy()

        # Temporary Status column
        working_df["Status"] = working_df["Faces Detected"].apply(
            lambda x: "Success" if x > 0 else "Failure"
        )

        total_images = len(working_df)

        success_df = working_df[working_df["Status"] == "Success"]

        detected = len(success_df)

        accuracy = (detected / total_images) * 100 if total_images else 0

        avg_latency = (
            success_df["Latency (ms)"].mean()
            if detected > 0
            else float("inf")
        )

        print(f"\n{model}")
        print(f"Total Images   : {total_images}")
        print(f"Faces Detected : {detected}")
        print(f"Accuracy       : {accuracy:.2f}%")
        print(f"Avg Latency    : {avg_latency:.2f} ms")

        return {
            "images": total_images,
            "faces": detected,
            "accuracy": round(accuracy, 2),
            "latency": round(avg_latency, 2),
        }

    def compare_models(self):

        print("\n========== SECUREFACE AI MODEL COMPARISON ==========\n")

        self.results.clear()

        for model in self.models:

            self.show_sample_results(model)

            result = self.read_results(model)

            if result:
                self.results[model] = result
            else:
                print(f"{model} results not found.")

        if not self.results:
            print("\nNo benchmark files found.")
            return

        comparison_df = pd.DataFrame(self.results).T

        comparison_df.rename(
            columns={
                "accuracy": "Accuracy (%)",
                "latency": "Latency (ms)",
                "faces": "Faces Detected",
                "images": "Total Images",
            },
            inplace=True,
        )

        print("\n")
        print("=" * 70)
        print("FINAL MODEL COMPARISON")
        print("=" * 70)
        print(comparison_df.to_string())

        # Best model = Highest Accuracy, Lowest Latency
        best_model = comparison_df.sort_values(
            by=["Accuracy (%)", "Latency (ms)"],
            ascending=[False, True],
        ).iloc[0]

        best_name = comparison_df.sort_values(
            by=["Accuracy (%)", "Latency (ms)"],
            ascending=[False, True],
        ).index[0]

        print("\n" + "=" * 60)
        print(f"BEST MODEL : {best_name}")
        print("=" * 60)

        print(f"Accuracy      : {best_model['Accuracy (%)']:.2f}%")
        print(f"Avg Latency   : {best_model['Latency (ms)']:.2f} ms")
        print(
            f"Faces Found   : {int(best_model['Faces Detected'])}/{int(best_model['Total Images'])}"
        )

        print("\nRecommendation:")

        if best_name == "RetinaFace":
            print("✔ Use RetinaFace in the final SecureFace AI system.")
            print("✔ Highest face detection accuracy.")
            print("✔ Suitable for secure face authentication.")

        elif best_name == "MediaPipe":
            print("✔ MediaPipe is the fastest model.")
            print("✔ Recommended for real-time applications.")

        else:
            print("✔ MTCNN provides a good balance of speed and accuracy.")
            print("✔ Recommended for systems with limited resources.")


if __name__ == "__main__":

    selector = ModelSelector()
    selector.compare_models()








'''


========== SECUREFACE AI MODEL COMPARISON ==========


==========================================================================================
MTCNN SAMPLE RESULTS (First 5 Rows)
==========================================================================================
  Image Name  Faces Detected  Latency (ms)  Status
1 (2916).jpg               1        456.78 Success
 1 (607).jpg               1        270.23 Success
1 (3767).jpg               0        266.18 Failure
 1 (576).jpg               1        281.11 Success
1 (1856).jpg               1        281.06 Success

MTCNN
Total Images   : 7219
Faces Detected : 6926
Accuracy       : 95.94%
Avg Latency    : 267.37 ms

==========================================================================================
MEDIAPIPE SAMPLE RESULTS (First 5 Rows)
==========================================================================================
 Image Name  Faces Detected  Latency (ms)  Status
 1 (1).jpeg               1         37.27 Success
  1 (1).jpg               1          6.52 Success
  1 (1).png               1          5.69 Success
1 (10).jpeg               1          6.24 Success
 1 (10).jpg               1          6.82 Success

MediaPipe
Total Images   : 7219
Faces Detected : 7116
Accuracy       : 98.57%
Avg Latency    : 8.40 ms

==========================================================================================
RETINAFACE SAMPLE RESULTS (First 5 Rows)
==========================================================================================
  Image Name  Faces Detected  Latency (ms)  Status
1 (2916).jpg               1        185.03 Success
 1 (607).jpg               1        172.22 Success
1 (3767).jpg               1        180.70 Success
 1 (576).jpg               0        170.83 Failure
1 (1856).jpg               1        173.59 Success

RetinaFace
Total Images   : 7219
Faces Detected : 5471
Accuracy       : 75.79%
Avg Latency    : 186.61 ms


======================================================================
FINAL MODEL COMPARISON
======================================================================
            Total Images  Faces Detected  Accuracy (%)  Latency (ms)
MTCNN             7219.0          6926.0         95.94        267.37
MediaPipe         7219.0          7116.0         98.57          8.40
RetinaFace        7219.0          5471.0         75.79        186.61

============================================================
BEST MODEL : MediaPipe
============================================================
Accuracy      : 98.57%
Avg Latency   : 8.40 ms
Faces Found   : 7116/7219

Recommendation:
✔ MediaPipe is the fastest model.
✔ Recommended for real-time applications.
'''