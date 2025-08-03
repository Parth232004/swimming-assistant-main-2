import pandas as pd
import json

def load_data():
    try:
        sessions = pd.read_csv("data/sessions.csv")
    except:
        sessions = pd.DataFrame(columns=["date", "user", "stroke", "distance", "fatigue", "mood", "feedback"])

    try:
        with open("data/users.json", "r") as f:
            users = json.load(f)
    except:
        users = {}
    return sessions, users

def save_data(sessions, users):
    sessions.to_csv("data/sessions.csv", index=False)
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=4)
