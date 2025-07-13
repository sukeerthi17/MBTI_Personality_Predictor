import streamlit as st
from collections import Counter
import joblib
import os
import matplotlib.pyplot as plt

# Load model and encoder
model = joblib.load("models/mbti_mcq_model.pkl")
label_encoder = joblib.load("models/mbti_label_encoder.pkl")

# Page config
st.set_page_config(page_title="MBTI Personality Predictor App", page_icon="🧠", layout="wide")
st.title("🧠 MBTI Personality Type Predictor")

# MBTI descriptions and quotes
mbti_info = {
    "INTJ": {"desc": "Strategic, logical, and visionary thinkers.", "quote": "“They can change the world.”"},
    "INTP": {"desc": "Innovative and deep thinkers.", "quote": "“Knowledge is power.”"},
    "ENTJ": {"desc": "Assertive leaders with big goals.", "quote": "“Vision into reality.”"},
    "ENTP": {"desc": "Curious idea generators.", "quote": "“Innovation leads.”"},
    "INFJ": {"desc": "Idealistic and insightful.", "quote": "“Look into your heart.”"},
    "INFP": {"desc": "Empathetic dreamers with strong values.", "quote": "“Follow your bliss.”"},
    "ENFJ": {"desc": "Altruistic and inspiring.", "quote": "“Make a difference.”"},
    "ENFP": {"desc": "Energetic and imaginative adventurers.", "quote": "“Do what you love.”"},
    "ISTJ": {"desc": "Organized and dependable realists.", "quote": "“Discipline = success.”"},
    "ISFJ": {"desc": "Loyal caretakers and helpers.", "quote": "“Lose yourself in service.”"},
    "ESTJ": {"desc": "Efficient and traditional organizers.", "quote": "“Plan and act.”"},
    "ESFJ": {"desc": "Supportive and community-driven.", "quote": "“We rise by lifting others.”"},
    "ISTP": {"desc": "Logical troubleshooters.", "quote": "“Leave your trail.”"},
    "ISFP": {"desc": "Artistic and gentle souls.", "quote": "“Be yourself.”"},
    "ESTP": {"desc": "Bold doers and action-takers.", "quote": "“Life is an adventure.”"},
    "ESFP": {"desc": "Joyful and spontaneous.", "quote": "“Enjoy the little things.”"}
}

# 15 Questions
questions = [
    {"question": "You prefer weekends that are:", "options": {
        "A": ("Alone reading a book", "I"), "B": ("Hanging with friends", "E"),
        "C": ("Family dinner", "E"), "D": ("Gaming solo", "I")}},
    {"question": "When solving a problem, you...", "options": {
        "A": ("Look at facts", "S"), "B": ("Trust your gut", "N"),
        "C": ("Visualize outcomes", "N"), "D": ("Use past experiences", "S")}},
    {"question": "You make decisions based on...", "options": {
        "A": ("Others’ feelings", "F"), "B": ("Logic", "T"),
        "C": ("Instinct", "F"), "D": ("Facts", "T")}},
    {"question": "Your schedule is usually...", "options": {
        "A": ("Planned", "J"), "B": ("Flexible", "P"),
        "C": ("Organized daily", "J"), "D": ("Spontaneous", "P")}},
    {"question": "In group work, you...", "options": {
        "A": ("Lead", "E"), "B": ("Listen", "I"),
        "C": ("Share ideas", "E"), "D": ("Observe", "I")}},
    {"question": "To recharge energy, you...", "options": {
        "A": ("Go out", "E"), "B": ("Stay home", "I"),
        "C": ("Events", "E"), "D": ("Watch something alone", "I")}},
    {"question": "You value more...", "options": {
        "A": ("Logic", "T"), "B": ("Compassion", "F"),
        "C": ("Truth", "T"), "D": ("Harmony", "F")}},
    {"question": "You trust more...", "options": {
        "A": ("Facts", "S"), "B": ("Dreams", "N"),
        "C": ("Data", "S"), "D": ("Intuition", "N")}},
    {"question": "Your work style is...", "options": {
        "A": ("Deadlines", "J"), "B": ("Last-minute", "P"),
        "C": ("Checklists", "J"), "D": ("Free-flow", "P")}},
    {"question": "In daily life you...", "options": {
        "A": ("Reflect", "I"), "B": ("Talk", "E"),
        "C": ("Stay quiet", "I"), "D": ("Socialize", "E")}},
    {"question": "New ideas excite you...", "options": {
        "A": ("Always", "N"), "B": ("If practical", "S"),
        "C": ("If they feel right", "N"), "D": ("If proven", "S")}},
    {"question": "You dislike...", "options": {
        "A": ("Disorganization", "J"), "B": ("Rigid plans", "P"),
        "C": ("Surprises", "J"), "D": ("Schedules", "P")}},
    {"question": "You communicate...", "options": {
        "A": ("Logically", "T"), "B": ("With empathy", "F"),
        "C": ("With structure", "T"), "D": ("With emotion", "F")}},
    {"question": "You prefer to...", "options": {
        "A": ("Act now", "P"), "B": ("Think first", "J"),
        "C": ("Adapt", "P"), "D": ("Organize", "J")}},
    {"question": "When traveling...", "options": {
        "A": ("Plan ahead", "J"), "B": ("Wing it", "P"),
        "C": ("Book early", "J"), "D": ("Go with flow", "P")}},
]

# Collect answers
answers = []
for i, q in enumerate(questions):
    st.markdown(f"**Q{i+1}. {q['question']}**")
    option_labels = [f"{k}) {v[0]}" for k, v in q["options"].items()]
    selected = st.radio("", option_labels, index=None, key=f"q{i}", horizontal=True)
    st.markdown('<hr style="margin-top: 1px; margin-bottom: 6px;">', unsafe_allow_html=True)
    selected_trait = None
    if selected:
        selected_key = selected[0]
        selected_trait = q["options"][selected_key][1]
    answers.append(selected_trait)


# Predict MBTI
if st.button("🎯 Predict My MBTI"):
    if None in answers:
        st.warning("❗ Please answer all 15 questions before submitting.")
    else:
        traits = Counter(answers)
        mbti_str = ''.join([
            'I' if traits['I'] > traits['E'] else 'E',
            'N' if traits['N'] > traits['S'] else 'S',
            'T' if traits['T'] > traits['F'] else 'F',
            'J' if traits['J'] > traits['P'] else 'P'
        ])

        binary_input = [
            int(mbti_str[0] == 'E'),
            int(mbti_str[1] == 'S'),
            int(mbti_str[2] == 'F'),
            int(mbti_str[3] == 'P')
        ]

        proba = model.predict_proba([binary_input])[0]
        pred_index = proba.argmax()
        pred_label = label_encoder.inverse_transform([pred_index])[0]
        confidence = proba[pred_index] * 100
        

        st.success(f"🧠 Based on your answers your MBTI type is: {mbti_str}")
    
        # Description & quote
        info = mbti_info.get(mbti_str)
        if info:
            st.markdown(f"📝 Description: _{info['desc']}_")
            st.info(f"💬 {info['quote']}")
        else:
            st.warning("ℹ️ No description found for this type.")

        # MBTI Image
        img_path = f"images/mbti_types/{mbti_str}.jpg"
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.warning("⚠️ No image found for this MBTI type.")

        # Charts
        st.subheader("📊 Trait Distribution")
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))

        # Bar Chart
        ax[0].bar(traits.keys(), traits.values(), color="skyblue")
        ax[0].set_title("Trait Counts")
        ax[0].set_ylabel("Count")
        ax[0].set_xlabel("Traits (I/E, N/S, T/F, J/P)")

        # Pie Chart
        trait_labels = list(traits.keys())
        trait_values = list(traits.values())
        ax[1].pie(trait_values, labels=trait_labels, autopct='%1.1f%%', startangle=90)
        ax[1].set_title("Trait Proportion")

        st.pyplot(fig)
