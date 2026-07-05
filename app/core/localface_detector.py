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
            min_detection_confidence=0.5,
            )
        
    def _is_looking_forward(self, detection):
        
        #Determines if the face is looking directly at the camera by checking 
        # if the nose is roughly centered between the left and right eyes.
        
        # Extract normalized keypoints
        right_eye = self.mp_face_detection.get_key_point(detection, self.mp_face_detection.FaceKeyPoint.RIGHT_EYE)
        left_eye = self.mp_face_detection.get_key_point(detection, self.mp_face_detection.FaceKeyPoint.LEFT_EYE)
        nose = self.mp_face_detection.get_key_point(detection, self.mp_face_detection.FaceKeyPoint.NOSE_TIP)

        # Calculate horizontal distances from the nose to each eye
        dist_right = abs(nose.x - right_eye.x)
        dist_left = abs(nose.x - left_eye.x)

        # Prevent division by zero if keypoints overlap entirely (unlikely but safe)
        if dist_right == 0 or dist_left == 0:
            return False

        # Calculate ratio of the smaller distance to the larger distance
        ratio = min(dist_left, dist_right) / max(dist_left, dist_right)

        # If the ratio is close to 1, the nose is perfectly centered. 
        # 0.6 is a good threshold for allowing slight, natural head tilts.
        return ratio > 0.6
    

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
            _is_looking_forward = False  # Initialize the looking forward flag
            if results.detections:
                h_frame,w_frame,_=frame.shape
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    x = int(bbox.xmin * w_frame)
                    y = int(bbox.ymin * h_frame)
                    w = int(bbox.width * w_frame)
                    h = int(bbox.height * h_frame)
                    faces.append((x, y, w, h))


                    # Evaluate if this specific face is looking forward
                    is_looking = self._is_looking_forward(detection)


                    #Eye detection
                    # Extract normalized eye keypoints
                    right_eye = self.mp_face_detection.get_key_point(
                        detection, self.mp_face_detection.FaceKeyPoint.RIGHT_EYE)
                    left_eye = self.mp_face_detection.get_key_point(
                        detection, self.mp_face_detection.FaceKeyPoint.LEFT_EYE)
                    nose = self.mp_face_detection.get_key_point(detection, self.mp_face_detection.FaceKeyPoint.NOSE_TIP)

                    # Convert normalized relative coordinates to absolute pixel coordinates
                    rx, ry = int(right_eye.x * w_frame), int(right_eye.y * h_frame)
                    lx, ly = int(left_eye.x * w_frame), int(left_eye.y * h_frame)
                    nx, ny = int(nose.x * w_frame), int(nose.y * h_frame)

                    # Draw circles over the eyes (Red for Right Eye, Blue for Left Eye)
                    cv.circle(frame, (rx, ry), 15, (0, 0, 255), 3) 
                    cv.circle(frame, (lx, ly), 15, (255, 0, 0), 3)
                    cv.circle(frame, (nx, ny), 10, (0, 255, 0), 2)  # Green for Nose


            for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 105, 65), 3)

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
