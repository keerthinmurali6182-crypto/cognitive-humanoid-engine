# Cognitive Humanoid Expression & Animation Engine

This repository contains an end-to-end processing pipeline for **Cognitive Humanoids and Digital Avatars**. The system ingests natural language text strings, leverages deep transformers to classify underlying emotional semantics, and translates those states into raw motor angles and structural 3D blendshapes in real time.

## ⚙️ Core Technical Highlights
* **Zero-Shot Emotional Processing:** Uses a `DistilBERT-MNLI` transformer model to extract human sentiment profiles dynamically across arbitrary text without requiring targeted training data.
* **Confidence-Scaled Kinematics:** Actuator positions are automatically scaled based on the classification confidence metric ($Position \times Confidence$). This creates a smoother, more realistic animation flow rather than sudden, jarring shifts.
* **Hardware Safe Boundary Enforcement:** Integrates a safety layer configuration that parses instructions through a clamping system to prevent motor damage or animation distortion.

## 🚀 Setup & Execution Guide
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Trigger the end-to-end cognitive runtime simulation loop
python src/simulation_app.py