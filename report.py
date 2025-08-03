import pandas as pd
import streamlit as st

def load_data(path='session_data/sessions.json'):
    try:
        return pd.read_json(path)
    except Exception:
        st.warning("No session data found.")
        return pd.DataFrame(columns=["date", "distance", "stroke", "mood"])

def show_reports():
    df = load_data()

    if df.empty:
        st.info("No data to show. Log some swim sessions first.")
        return

    st.subheader("📊 Distance Over Time")
    st.line_chart(df["distance"])

    st.subheader("🏊 Stroke Usage")
    st.bar_chart(df["stroke"].value_counts())

    st.subheader("😊 Mood Trends")
    mood_map = {"happy": 1, "tired": -1, "neutral": 0}
    df["mood_score"] = df["mood"].map(mood_map)
    st.line_chart(df["mood_score"])
