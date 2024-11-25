import math
import cv2

class JointUtils:

    frame = None
    landmarks = None

    @staticmethod
    def calculate_angle(a, b, c, invert=False):

        joint_a = JointUtils.landmarks[a]
        joint_b = JointUtils.landmarks[b]
        joint_c = JointUtils.landmarks[c]

        # Calculates the angle (in degrees) between three joints 
        radians = math.atan2(joint_c.y - joint_b.y, joint_c.x - joint_b.x) - math.atan2(joint_a.y - joint_b.y, joint_a.x - joint_b.x)
        angle = math.degrees(radians)
        angle = angle + 360 if angle < 0 else angle  # Ensure angle is within 0-360
        if invert:
            angle = 360 - angle if angle > 180 else angle
        
        # If an angle is being calculated, add it to frame
        JointUtils.add_angle_to_frame(JointUtils.frame, angle, joint_b)

        return angle

    @staticmethod
    def add_angle_to_frame(frame, angle, joint):
        """
        Adds an angle value to the frame at the position of a joint.
        frame: The video frame.
        angle: The angle value to display.
        joint: The Mediapipe landmark for the joint (with x and y attributes).
        """
        frame_height, frame_width, _ = frame.shape
        x = int(joint.x * frame_width)
        y = int(joint.y * frame_height)
        cv2.putText(frame, f'{int(angle)}deg', (x, y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
