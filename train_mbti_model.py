import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Create models folder if needed
os.makedirs("models", exist_ok=True)

# Load dataset
df = pd.read_csv("data/mbti_mcq_dataset.csv")

# Convert numeric MBTI column (0–15) into actual type strings
mbti_map = {
    0: "ISTJ", 1: "ISFJ", 2: "INFJ", 3: "INTJ",
    4: "ISTP", 5: "ISFP", 6: "INFP", 7: "INTP",
    8: "ESTP", 9: "ESFP", 10: "ENFP", 11: "ENTP",
    12: "ESTJ", 13: "ESFJ", 14: "ENFJ", 15: "ENTJ"
}
df["MBTI"] = df["MBTI"].map(mbti_map)  # ← convert numbers to strings

# Prepare features and labels
X = df[["IE", "NS", "TF", "JP"]]
y = df["MBTI"]

# Encode MBTI strings
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y_encoded)

# Save model & encoder
joblib.dump(model, "models/mbti_mcq_model.pkl")
joblib.dump(label_encoder, "models/mbti_label_encoder.pkl")

print("✅ Model and encoder saved.")
