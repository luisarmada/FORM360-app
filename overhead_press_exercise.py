from exercise import Exercise
from joint_utils import JointUtils

class OverheadPressExercise(Exercise):
    
    def detect_reps(self):

        # Calculate elbow angle
        left_elbow_angle = JointUtils.calculate_angle('left_shoulder', 'left_elbow', 'left_wrist', invert = True)
        right_elbow_angle = JointUtils.calculate_angle('right_shoulder', 'right_elbow', 'right_wrist')

        left_shoulder_angle = JointUtils.calculate_angle('left_elbow', 'left_shoulder', 'right_shoulder', invert = True)
        right_shoulder_angle = JointUtils.calculate_angle('right_elbow', 'right_shoulder', 'left_shoulder', invert = True)

        # Check rep logic
        # Initial Phase

        down_phase = self.almost_equal(left_elbow_angle, 90, epsilon = 20) and self.almost_equal(left_shoulder_angle, 180, epsilon = 20) and self.almost_equal(right_shoulder_angle, 180, epsilon = 20) and self.almost_equal(right_elbow_angle, 90, epsilon = 20)
        if self.current_phase == None:
            if down_phase == True:
                # self.current_phase = 'up_phase'
                self.increment_rep()

        return self.rep_count
