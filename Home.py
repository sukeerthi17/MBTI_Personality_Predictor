import streamlit as st

# Page configuration
st.set_page_config(
    page_title="MBTI Personality Predictor App",
    page_icon="🧠",
    layout="wide"
)

# Title and image
st.title("🧠 MBTI Personality Type Predictor")
st.image("images/mbti_full_chart.jpeg", use_container_width=True)

# Intro
st.markdown("""
Welcome to the AI-powered MBTI Personality Quiz!  
This tool helps you identify your Myers-Briggs Personality Type based on your choices.

👉 Navigate to "Check My MBTI" from the sidebar to begin the quiz.
""")

st.markdown("---")

# MBTI Trait Descriptions
st.subheader("1. Extraversion (E) vs. Introversion (I)")
st.markdown("""
- 🟢 Extraversion (E): Outgoing, expressive, and energized by social interaction.  
- 🟢 Introversion (I): Reserved, reflective, and energized by solitude.
""")

st.subheader("2. Sensing (S) vs. Intuition (N)")
st.markdown("""
- 🟢 Sensing (S): Relies on present details and facts.  
- 🟢 Intuition (N): Focuses on patterns, possibilities, and future insights.
""")

st.subheader("3. Thinking (T) vs. Feeling (F)")
st.markdown("""
- 🟢 Thinking (T): Logical, objective, and values fairness.  
- 🟢 Feeling (F): Compassionate, values emotions and harmony.
""")

st.subheader("4. Judging (J) vs. Perceiving (P)")
st.markdown("""
- 🟢 Judging (J): Prefers order, structure, and planning.  
- 🟢 Perceiving (P): Flexible, adaptable, and spontaneous.
""")
