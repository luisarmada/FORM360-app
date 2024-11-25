import cv2
import mediapipe as mp

class PoseRenderer:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def process_frame(self, frame):
        """
        Processes the frame to detect pose landmarks.
        Returns the processed results and the flipped frame.
        """
        flipped_frame = cv2.flip(frame, 1)  # Flip horizontally for mirror effect
        rgb_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        return results, flipped_frame

    def swap_landmarks_for_mirror(self, landmarks):
        """
        Swaps landmarks for mirrored feed (left and right sides).
        Returns swapped landmarks.
        """
        left_shoulder, right_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER], \
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_elbow, right_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW], \
                                  landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
        left_wrist, right_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST], \
                                  landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]

        return {
            'left_shoulder': right_shoulder,
            'right_shoulder': left_shoulder,
            'left_elbow': right_elbow,
            'right_elbow': left_elbow,
            'left_wrist': right_wrist,
            'right_wrist': left_wrist
        }
