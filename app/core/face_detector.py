import cv2 as cv
import mediapipe as mp
import gc

class Detect_face:
    def __init__(self):
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

        # Calculate horizontal distances between nose to each eye
        dist_right = abs(nose.x - right_eye.x)
        dist_left = abs(nose.x - left_eye.x)

        # Prevent division by zero if keypoints overlap entirely 
        if dist_right == 0 or dist_left == 0:
            return False

        # Calculate ratio of the smaller distance to the larger distance
        ratio = min(dist_left, dist_right) / max(dist_left, dist_right)

        # If the ratio is close to 1, the nose is perfectly centered. 
        # 0.6 is a good threshold for allowing slight, natural head tilts.
        return ratio > 0.6
    

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

    def detect(self,frame):

        #Process the frame for face detection in RGB
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.detector.process(rgb)


        faces = []
        h_frame,w_frame,_=frame.shape
        is_forward = False
        forward_faces_count = 0
        if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    x = int(bbox.xmin * w_frame)
                    y = int(bbox.ymin * h_frame)
                    w = int(bbox.width * w_frame)
                    h = int(bbox.height * h_frame)

                    #Add face to the list of detected face
                    faces.append((x, y, w, h))

                    is_forward = self._is_looking_forward(detection)
                    if(is_forward):
                        forward_faces_count += 1
        del results
        results=None
        if len(faces) == 0:
            del rgb  # Free memory array
            gc.collect()
            return {
                "success": False,
                "message": "No face detected.",
                "faces": [],
                "face": None
            }

        if len(faces) > 1:
            del rgb  # Free memory array
            gc.collect()
            return {
                "success": False,
                "message": "Multiple faces detected.",
                "faces": faces,
                "face": None
            }

        if not is_forward and forward_faces_count == 0:
            del rgb  # Free memory array
            gc.collect()
            return {
                "success": False,
                "message": "Please look straight at the camera.",
                "faces": faces,
                "face": None
            }
        
        # x, y, w, h = faces[0]
        # x = max(0, x)
        # y = max(0, y)

        

        return {

            "success": True,

            "message": "Face Detected",

            "faces": faces,

            "face": rgb,

            # "bbox": (x, y, w, h)
        }
        

#To run tthe class
if __name__ == "__main__":
    detector = Detect_face()
    detector.start_validation_stream()
