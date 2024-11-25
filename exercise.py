class Exercise:
    def __init__(self):
        self.rep_count = 0
        self.current_phase = None

    def increment_rep(self):
        self.rep_count += 1
        print(f"Rep completed! Total reps: {self.rep_count}")

    def almost_equal(self, a, b, epsilon=1e-6):
        return abs(a - b) <= epsilon


    def detect_reps(self):
        # Override this method in subclasses for specific exercises.
        pass
