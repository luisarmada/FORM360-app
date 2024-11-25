import cv2
import mediapipe as mp
import math

# Initialize Mediapipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to calculate the angle between three joints
def calculate_angle(joint_a, joint_b, joint_c, invert=False):
    """
    Calculates the angle (in degrees) between three joints:
    joint_a, joint_b (vertex), joint_c.
    If invert=True, flips the angle to ensure anatomical consistency.
    """
    radians = math.atan2(joint_c.y - joint_b.y, joint_c.x - joint_b.x) - math.atan2(joint_a.y - joint_b.y, joint_a.x - joint_b.x)
    angle = math.degrees(radians)
    angle = angle + 360 if angle < 0 else angle  # Ensure angle is within 0-360

    # Flip the angle if needed
    if invert:
        angle = 360 - angle if angle > 180 else angle

    return angle

# Function to add the angle value to the frame
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

# Open the default camera
cam = cv2.VideoCapture(0)

# Initialize Mediapipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        ret, frame = cam.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Flip the frame horizontally for a mirror effect
        flipped_frame = cv2.flip(frame, 1)

        # Convert the flipped frame to RGB (required by Mediapipe)
        rgb_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)

        # Process the frame to detect pose landmarks
        results = pose.process(rgb_frame)

        # If pose landmarks are detected
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmarks for left and right sides
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

            # Swap landmarks for mirrored feed
            left_shoulder, right_shoulder = right_shoulder, left_shoulder
            left_elbow, right_elbow = right_elbow, left_elbow
            left_wrist, right_wrist = right_wrist, left_wrist

            # Calculate elbow angles
            elbow_angle_left = calculate_angle(left_shoulder, left_elbow, left_wrist, invert=True)
            elbow_angle_right = calculate_angle(right_shoulder, right_elbow, right_wrist)
            shoulder_angle_left = calculate_angle(left_elbow, left_shoulder, right_shoulder)
            shoulder_angle_right = calculate_angle(left_shoulder, right_shoulder, right_elbow)

            # Add angles to the frame
            add_angle_to_frame(flipped_frame, elbow_angle_left, left_elbow)
            add_angle_to_frame(flipped_frame, elbow_angle_right, right_elbow)
            add_angle_to_frame(flipped_frame, shoulder_angle_left, left_shoulder)
            add_angle_to_frame(flipped_frame, shoulder_angle_right, right_shoulder)

            # Draw landmarks and connections on the frame
            mp_drawing.draw_landmarks(
                flipped_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
            )

        # Display the flipped frame
        cv2.imshow('Pose Detection with Angles', flipped_frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break

# Release the capture object
cam.release()
cv2.destroyAllWindows()
