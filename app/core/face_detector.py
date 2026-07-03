import cv2 as cv
import mediapipe as mp


class Detect_face:
    def __init__(self, camera_index=0):
        self.cap = cv.VideoCapture(camera_index)
        self.last_status = None  # Tracks status changes to avoid flooding the terminal
        
        #Initializing mediapipeface detection model
        self.mp_face_detection = mp.solutions.face_detection

        self.detector = self.mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5
        )

    def start_validation_stream(self):
        #Opens camera loop and validates the user face in real-time.
        if not self.cap.isOpened():
            print("Error: Cannot open camera")
            return False

        print("\n--- Dectector Stream Started ---")
        print("Press 'q' inside the camera window to exit.\n")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            clean_frame=frame.copy()

            #Process the frame for face detection in RGB
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = self.detector.process(rgb)

            #Draw bounding boxes
            faces = []
            if results.detections:
                h_frame,w_frame,_=frame.shape
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    x = int(bbox.xmin * w_frame)
                    y = int(bbox.ymin * h_frame)
                    w = int(bbox.width * w_frame)
                    h = int(bbox.height * h_frame)
                    faces.append((x, y, w, h))

            for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Display frame
            cv.imshow('Detector Screen', frame)

            #Validate face count logic
            is_valid = self._validate_face_count(len(faces))
            
            if is_valid: 
                # return True

                print("\n[SUCCESS] Capturing Image!")
                
                # Save the full clean frame
                cv.imwrite("captured_full_frame.jpg", clean_frame)
                
                # Crop the face and save it separately
                x, y, w, h = faces[0]
                cropped_face = clean_frame[y:y+h, x:x+w]
                cv.imwrite("captured_cropped_face.jpg", cropped_face)
                
                print("-> Saved 'captured_full_frame.jpg'")
                print("-> Saved 'captured_cropped_face.jpg'")

            if cv.waitKey(1) == ord('q'):
                break

        self.cleanup()

    def _validate_face_count(self, face_count):
        #Cehcks only 1 face exists
        status = "valid"
        
        if face_count == 0:
            status = "no_face"
            message = "Validation Failed: No clear face detected. Please ensure good lighting and look directly at the camera."
        elif face_count > 1:
            status = "multiple_faces"
            message = f"Validation Failed: {face_count} faces detected. Authentication requires exactly 1 person in the frame."
        else:
            message = "Validation Passed: 1 face detected. Proceeding..."

        # Only print if the status changes (prevents spamming the terminal 30 times a second)
        if status != self.last_status:
            print(message)
            self.last_status = status

        return status == "valid"

    def cleanup(self):
        #Safely release camera and close UI windows.
        if self.cap.isOpened():
            self.cap.release()
        cv.destroyAllWindows()
        print("Camera resources released successfully.")


#To run tthe class
if __name__ == "__main__":
    detector = Detect_face(camera_index=0)
    detector.start_validation_stream()
