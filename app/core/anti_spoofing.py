import math
import cv2
import time
import numpy as np
import mediapipe as mp


class LivenessDetector:
    def __init__(self):
        # Setup MediaPipe Face Mesh to find face points
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        # Cutoff thresholds
        self.blink_close_limit = 0.23
        self.blink_open_limit = 0.26
        self.turn_limit = 18.0
        self.tilt_limit = 12.0

        # Landmark IDs for the eyes
        self.left_eye_points = [362, 385, 387, 263, 373, 380]
        self.right_eye_points = [33, 160, 158, 133, 153, 144]

        # 3D points of a standard human face (in millimeters)
        self.face_3d_model = np.array(
            [
                (0.0, 0.0, 0.0),             # Nose tip
                (0.0, -330.0, -65.0),        # Chin
                (-225.0, 170.0, -135.0),     # Left corner of left eye
                (225.0, 170.0, -135.0),      # Right corner of right eye
                (-150.0, -150.0, -125.0),    # Left corner of mouth
                (150.0, -150.0, -125.0),     # Right corner of mouth
            ],
            dtype=np.float64,
        )

        # Variables to track blinking over time
        self.eye_state = "OPEN"
        self.frames_closed = 0
        self.blink_count = 0
        self.last_blink_time = 0.0

    def _get_distance(self, pt1, pt2):
        # Simple Pythagorean distance between two 2D points.
        return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    def _calculate_eye_ratio(self, landmarks, eye_points, width, height):
        # Measures how open an eye is (Eye Aspect Ratio).
        # Convert points from 0.0-1.0 percentages to actual pixel values
        pts = []
        for idx in eye_points:
            px = landmarks[idx].x * width
            py = landmarks[idx].y * height
            pts.append((px, py))

        # Vertical distances between top and bottom eyelids
        top_bottom_1 = self._get_distance(pts[1], pts[5])
        top_bottom_2 = self._get_distance(pts[2], pts[4])

        # Horizontal distance between eye corners
        left_right = self._get_distance(pts[0], pts[3])

        if left_right == 0:
            return 0.0

        # Return the open/close ratio
        return (top_bottom_1 + top_bottom_2) / (2.0 * left_right)

    def _get_head_angles(self, landmarks, width, height):
        # checks if head is turning left/right or up/down.
        # Grab the 6 matching points from the detected face on screen
        face_2d_points = np.array(
            [
                (landmarks[1].x * width, landmarks[1].y * height),     # Nose tip
                (landmarks[199].x * width, landmarks[199].y * height), # Chin
                (landmarks[33].x * width, landmarks[33].y * height),   # Left eye corner
                (landmarks[263].x * width, landmarks[263].y * height), # Right eye corner
                (landmarks[61].x * width, landmarks[61].y * height),   # Left mouth corner
                (landmarks[291].x * width, landmarks[291].y * height), # Right mouth corner
            ],
            dtype=np.float64,
        )

        # Standard basic camera setup
        focal_length = width
        center = (width / 2, height / 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]],
            dtype=np.float64,
        )
        dist_matrix = np.zeros((4, 1))

        # Match 2D image points to our 3D model
        success, rot_vec, _ = cv2.solvePnP(
            self.face_3d_model, face_2d_points, camera_matrix, dist_matrix
        )
        if not success:
            return 0.0, 0.0

        # Convert rotation matrix to readable degrees
        rot_matrix, _ = cv2.Rodrigues(rot_vec)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rot_matrix)

        pitch = round(angles[0], 1)  # Up and Down
        yaw = round(angles[1], 1)    # Left and Right

        return yaw, pitch

    def _update_blinks(self, ear_score):
        # count a blink when eyes open closed and again open. 
        if self.eye_state == "OPEN":
            if ear_score < self.blink_close_limit:
                self.eye_state = "CLOSED"
                self.frames_closed = 1

        elif self.eye_state == "CLOSED":
            if ear_score < self.blink_close_limit:
                self.frames_closed += 1
                # If eyes stay shut too long (>10 frames), it's a photo or sleep, not a blink
                if self.frames_closed > 10:
                    self.eye_state = "OPEN"
                    self.frames_closed = 0
            else:
                # Eye opened again within 1-10 frames -> genuine blink!
                if 1 <= self.frames_closed <= 10:
                    self.blink_count += 1
                    self.last_blink_time = time.time()
                self.eye_state = "OPEN"
                self.frames_closed = 0

# main script for checking liveness 
    def check_liveness(self, frame):
        # checks one camera frame and checks for liveness 
        height, width, _ = frame.shape

        # MediaPipe needs RGB format
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb_image)

        # If no face is visible
        if not result.multi_face_landmarks:
            self.no_face_frames += 1
            # Reset only after 5 consecutive missing frames (grace period)
            if self.no_face_frames > 5:
                self.reset()
            return {
                "face_detected": False,
                "is_live": False,
                "ear": 0.0,
                "blink_count": self.blink_count,
                "head_direction": "NONE",
                "yaw": 0.0,
                "pitch": 0.0,
            }

        face_points = result.multi_face_landmarks[0].landmark

        # Step 1: Check Eye Openness
        left_eye_ear = self._calculate_eye_ratio(face_points, self.left_eye_points, width, height)
        right_eye_ear = self._calculate_eye_ratio(face_points, self.right_eye_points, width, height)
        avg_ear = round((left_eye_ear + right_eye_ear) / 2.0, 2)

        # Step 2: Track Blink Count
        self._update_blinks(avg_ear)

        # Step 3: Check Head Rotation
        yaw, pitch = self._get_head_angles(face_points, width, height)

        # Step 4: Simple direction labels
        if yaw > self.turn_limit:
            direction = "RIGHT"
        elif yaw < -self.turn_limit:
            direction = "LEFT"
        elif pitch > self.tilt_limit:
            direction = "UP"
        elif pitch < -self.tilt_limit:
            direction = "DOWN"
        else:
            direction = "FORWARD"

        time_since_last_blink = time.time() - self.last_blink_time
        is_currently_live = (self.blink_count >= 1) and (time_since_last_blink < 3.5)

        return {
            "face_detected": True,
            "is_live": is_currently_live,  # True once at least 1 blink is detected
            "ear": avg_ear,
            "blink_count": self.blink_count,
            "head_direction": direction,
            "yaw": yaw,
            "pitch": pitch,
        }

    def reset(self):
        # reset the counter variable for new user checks
        self.eye_state = "OPEN"
        self.frames_closed = 0
        self.blink_count = 0
        self.last_blink_time = 0.0