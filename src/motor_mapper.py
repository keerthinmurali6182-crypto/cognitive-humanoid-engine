class MotorActuatorMapper:
    def __init__(self, config: dict):
        self.config = config['emotion_map']
        self.limits = config['motor_limits']

    def calculate_rig_positions(self, cognitive_intent: dict) -> dict:
        """
        Maps abstract emotional states into precise hardware motor positions and blendshapes.
        """
        emotion = cognitive_intent["emotion"]
        confidence = cognitive_intent["confidence"]

        # Default to neutral if anomalous emotion state is passed
        target_profile = self.config.get(emotion, self.config["neutral"])

        # Interpolate raw motor positions scaled by the confidence of the detected sentiment
        calculated_neck_pitch = target_profile["neck_pitch"] * confidence
        calculated_eyebrow_lift = target_profile["eyebrow_lift"] * confidence
        calculated_jaw_open = target_profile["jaw_open"] * confidence

        # Enforce physical hardware constraints to prevent mechanical stress
        final_neck_pitch = max(min(calculated_neck_pitch, self.limits["neck_pitch_max"]), -self.limits["neck_pitch_max"])
        final_eyebrow_lift = max(min(calculated_eyebrow_lift, self.limits["eyebrow_lift_max"]), 0.0)
        final_jaw_open = max(min(calculated_jaw_open, 1.0), 0.0)

        return {
            "actuators": {
                "neck_motor_pitch_deg": round(final_neck_pitch, 2),
                "neck_motor_yaw_deg": 0.0  # Kept static for basic front-facing speech simulation
            },
            "blendshapes": {
                "eyebrow_lift_coefficient": round(final_eyebrow_lift, 2),
                "jaw_open_coefficient": round(final_jaw_open, 2)
            }
        }