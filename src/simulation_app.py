import os
# 1. Suppress the Hugging Face symlink warning on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import time
from transformers import pipeline

print("Initializing Cognitive Humanoid NLP Layer...")

# Initialize the zero-shot classification pipeline
# (Ensure your HF_TOKEN is set in your system environment variables to clear the other warning)
classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

# 2. Expanded candidate labels to include a baseline 'neutral' state
CANDIDATE_LABELS = ["joy", "anger", "sadness", "neutral"]

# 3. Define a confidence threshold (e.g., 60%) to filter out weak inferences
CONFIDENCE_THRESHOLD = 0.60

def get_motor_coordinates(state):
    """Maps the recognized primary emotional state to hardware targets."""
    # Default / Neutral baseline values
    coordinates = {
        'servo_motors': {'neck_motor_pitch_deg': 0.0, 'neck_motor_yaw_deg': 0.0},
        'mesh_blendshapes': {'eyebrow_lift_coefficient': 0.0, 'jaw_open_coefficient': 0.0}
    }
    
    if state == "joy":
        coordinates['servo_motors'] = {'neck_motor_pitch_deg': 9.92, 'neck_motor_yaw_deg': 0.0}
        coordinates['mesh_blendshapes'] = {'eyebrow_lift_coefficient': 0.79, 'jaw_open_coefficient': 0.3}
    elif state == "anger":
        coordinates['servo_motors'] = {'neck_motor_pitch_deg': -4.95, 'neck_motor_yaw_deg': 0.0}
        coordinates['mesh_blendshapes'] = {'eyebrow_lift_coefficient': 0.0, 'jaw_open_coefficient': 0.1}
    elif state == "sadness":
        coordinates['servo_motors'] = {'neck_motor_pitch_deg': -5.63, 'neck_motor_yaw_deg': 0.0}
        coordinates['mesh_blendshapes'] = {'eyebrow_lift_coefficient': 0.03, 'jaw_open_coefficient': 0.0}
        
    return coordinates

print("\n🚀 Commencing Cognitive Humanoid Evaluation Loop...\n")

# Simulated stream of human inputs for testing
voice_stream_inputs = [
    "Wow, this is absolutely incredible news! I am so thrilled with this result!",
    "I am really frustrated with how poorly this script is performing right now.",
    "The operations department will update the maintenance logs at five o'clock tomorrow afternoon."
]

for text in voice_stream_inputs:
    print(f'[Human Input Voice Stream]: "{text}"')
    
    # Run inference
    result = classifier(text, candidate_labels=CANDIDATE_LABELS)
    
    primary_state = result['labels'][0]
    confidence = result['scores'][0]
    
    # 4. Threshold gating check
    if confidence < CONFIDENCE_THRESHOLD:
        # Fallback to neutral if the model is guessing blindly
        primary_state = "neutral"
        
    print(f"🧠 Cognitive Analysis -> Primary State: {primary_state} (Confidence: {confidence * 100:.1f}%)")
    
    # Fetch coordinates based on filtered/validated state
    hardware_targets = get_motor_coordinates(primary_state)
    
    print("🤖 Dispatched Physical Humanoid Motor Coordinates:")
    print(f"   ↳ Servo Motors:  {hardware_targets['servo_motors']}")
    print(f"   ↳ Mesh Blendshapes: {hardware_targets['mesh_blendshapes']}\n")
    
    time.sleep(1) # Simulating spacing between inputs