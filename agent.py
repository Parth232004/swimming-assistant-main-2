import pandas as pd
import random

class SwimCoachAgent:
    def __init__(self, session_data, user_data, user):
        self.df = session_data
        self.user_data = user_data
        self.user = user
        self.memory = self.df[self.df['user'] == user].copy()

    def get_trend(self):
        if len(self.memory) < 2:
            return "neutral"
        recent = self.memory.tail(3)
        fatigue = recent['fatigue'].mean()
        dist_change = recent['distance'].diff().mean()
        if fatigue >= 7:
            return "fatigued"
        elif dist_change > 50:
            return "improving"
        elif dist_change < -50:
            return "declining"
        return "neutral"

    def generate_suggestion(self):
        trend = self.get_trend()
        suggestion = ""
        if trend == "improving":
            suggestion = "Great job! Try increasing your distance by 100m today."
        elif trend == "fatigued":
            suggestion = "You seem tired. Take a light 400m swim today."
        elif trend == "declining":
            suggestion = "Let’s get back on track. Try a moderate 600m swim today."
        else:
            suggestion = "Keep your pace. Try the usual 700m today."

        return suggestion

    def update_score(self, feedback):
        if feedback == "👍":
            self.user_data[self.user]["score"] += 1
        elif feedback == "👎":
            self.user_data[self.user]["score"] = max(0, self.user_data[self.user]["score"] - 1)
