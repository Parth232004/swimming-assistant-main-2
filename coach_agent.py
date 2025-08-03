import os
import json
import pandas as pd

class CoachAgent:
    def __init__(self):
        self.session_file = "data/sessions.csv"
        self.feedback_file = "data/feedback.json"

        # Ensure the data directory and files exist
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.session_file):
            pd.DataFrame(columns=["date", "stroke", "distance", "fatigue"]).to_csv(self.session_file, index=False)

        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, "w") as f:
                json.dump({}, f)

        # Load sessions into memory
        self.sessions = pd.read_csv(self.session_file)

    def suggest(self):
        # Basic suggestion logic based on fatigue
        if self.sessions.empty:
            return "How about 500m of freestyle to get started?"

        last = self.sessions.iloc[-1]
        if last["fatigue"] == "high":
            return "Take it light today. Try 300m backstroke with breaks."
        elif last["fatigue"] == "medium":
            return "How about 750m of freestyle today?"
        else:
            return "Push your limits with 1000m freestyle and sprints!"

    def record_feedback(self, was_helpful, mood):
        with open(self.feedback_file, "r") as f:
            feedback = json.load(f)

        key = f"feedback_{len(feedback)+1}"
        feedback[key] = {
            "was_helpful": was_helpful,
            "mood": mood
        }

        with open(self.feedback_file, "w") as f:
            json.dump(feedback, f, indent=2)
