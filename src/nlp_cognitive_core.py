from transformers import pipeline

class CognitiveProcessor:
    def __init__(self):
        print("Initializing Cognitive Humanoid NLP Layer...")
        # Load a highly efficient, lightweight sentiment model
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="typeform/distilbert-base-uncased-mnli"
        )
        # Bounded cognitive states supported by our motor rig
        self.candidate_labels = ["joy", "sadness", "anger", "neutral"]

    def analyze_input_intent(self, text: str) -> dict:
        """
        Parses raw human dialogue text to extract structural emotional intent vectors.
        """
        if not text.strip():
            return {"emotion": "neutral", "confidence": 1.0}

        inference_result = self.classifier(text, candidate_labels=self.candidate_labels)
        
        # Pull the top matching class designation
        top_emotion = inference_result['labels'][0]
        confidence_score = inference_result['scores'][0]

        return {
            "emotion": top_emotion,
            "confidence": float(confidence_score)
        }