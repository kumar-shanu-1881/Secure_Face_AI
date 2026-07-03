import cv2 as cv

class Detect_face:
    def __init__(self, camera_index=0):
        #Initialize the cap object(camera) haarcascademodel 
        self.cap = cv.VideoCapture(camera_index)
        self.face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.last_status = None  # Tracks status changes to avoid flooding the terminal

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

            #Process the frame for face detection
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(30, 30))

            #Draw bounding boxes
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
