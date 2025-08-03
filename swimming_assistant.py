import json
import os
import datetime
import matplotlib.pyplot as plt

DATA_FILE = "swim_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"sessions": [], "adjustment": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_session(data):
    print("\n=== Swimming Session Logging ===")
    distance = int(input("Enter today's swimming distance (in meters): "))
    swim_type = input("Enter swim type (freestyle/backstroke/etc.): ")
    fatigue = int(input("Rate your fatigue (1-10): "))

    session = {
        "date": str(datetime.date.today()),
        "distance": distance,
        "type": swim_type,
        "fatigue": fatigue
    }
    data["sessions"].append(session)

    # RL-like adjustment
    if fatigue > 7:
        data["adjustment"] -= 50
    elif fatigue < 4:
        data["adjustment"] += 50

    save_data(data)
    return distance, fatigue

def give_feedback(distance, fatigue, adjustment):
    suggestion = distance + adjustment
    if suggestion < 0:
        suggestion = 0
    print("\n=== AI Coach Feedback ===")
    if fatigue > 7:
        print(f"You seem tired. Tomorrow, reduce by {abs(adjustment)}m and focus on form.")
    elif fatigue < 4:
        print(f"Great energy! You can increase by {abs(adjustment)}m tomorrow.")
    else:
        print("Balanced effort today. Keep maintaining your rhythm.")
    print(f"Suggested distance for next session: {suggestion}m")

def weekly_summary(data):
    if not data["sessions"]:
        print("No data yet to show summary.")
        return
    sessions = data["sessions"][-7:]
    dates = [s["date"] for s in sessions]
    distances = [s["distance"] for s in sessions]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, distances, marker="o", color="blue", linewidth=2)
    plt.title("Weekly Swimming Distance")
    plt.xlabel("Date")
    plt.ylabel("Distance (m)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    data = load_data()
    while True:
        print("\n--- Swimming Assistant ---")
        print("1. Log today's session")
        print("2. View weekly summary")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            distance, fatigue = log_session(data)
            give_feedback(distance, fatigue, data["adjustment"])
        elif choice == "2":
            weekly_summary(data)
        elif choice == "3":
            print("Goodbye! Keep swimming strong!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
