import streamlit as st

def feedback_form():
    st.subheader("🗣️ Post-Swim Feedback")
    feedback = st.radio("Was today’s suggestion helpful?", ["👍", "👎"])
    mood = st.radio("How did you feel after today’s swim?", ["happy", "tired", "neutral"])
    return feedback, mood
