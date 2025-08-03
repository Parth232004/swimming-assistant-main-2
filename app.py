# app.py
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from coach_agent import CoachAgent

st.set_page_config(page_title="CoachAI", layout="centered")

# Instantiate the agent
agent = CoachAgent()

# App title
st.title("🏊 CoachAI Test App")
st.header("Hello Parth! Your Streamlit app is running successfully.")

# Suggestion section
st.subheader("🤖 Today's Smart Suggestion:")
st.write(agent.suggest())

# Record a new session
st.subheader("📋 Enter Today’s Session")
with st.form("session_form"):
    date = st.date_input("Date")
    stroke = st.selectbox("Stroke", ["freestyle", "backstroke", "breaststroke", "butterfly"])
    distance = st.number_input("Distance (meters)", min_value=0, step=50)
    fatigue = st.selectbox("Fatigue Level", ["low", "medium", "high"])
    submit = st.form_submit_button("Save Session")

    if submit:
        new_session = {
            "date": date.strftime('%Y-%m-%d'),
            "stroke": stroke,
            "distance": distance,
            "fatigue": fatigue
        }
        # Append to CSV file
        df = pd.read_csv(agent.session_file) if os.path.exists(agent.session_file) else pd.DataFrame()
        df = pd.concat([df, pd.DataFrame([new_session])], ignore_index=True)
        df.to_csv(agent.session_file, index=False)
        st.success("✅ Session saved successfully!")

# Feedback section
st.subheader("💬 Feedback on Suggestion")
col1, col2 = st.columns(2)
with col1:
    helpful = st.button("👍 Helpful")
with col2:
    not_helpful = st.button("👎 Not Helpful")

mood = st.selectbox("How did you feel after the swim?", ["😌 Great", "😐 Okay", "😣 Tired"])

if helpful or not_helpful:
    was_helpful = True if helpful else False
    agent.record_feedback(was_helpful=was_helpful, mood=mood)
    st.success("✅ Feedback recorded. Thanks!")

# Progress Reports
st.subheader("📊 Progress Reports")

# Load and plot session data
if os.path.exists(agent.session_file):
    df = pd.read_csv(agent.session_file)

    if not df.empty:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date', 'distance'])

        df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
        df = df.dropna(subset=['distance'])

        # Group by date
        distance_per_day = df.groupby('date')['distance'].sum()

        # Plot using matplotlib to avoid st.pyplot() warning
        fig, ax = plt.subplots()
        distance_per_day.plot(kind='line', marker='o', ax=ax)
        ax.set_title("Total Distance per Day")
        ax.set_xlabel("Date")
        ax.set_ylabel("Distance (m)")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.info("No session data available yet.")
else:
    st.info("No sessions recorded yet.")
