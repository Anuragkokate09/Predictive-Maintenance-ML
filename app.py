import streamlit as st
import pandas as pd
import joblib
import os

# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="Predictive Maintenance",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Machine Failure Prediction")
st.write("Industry 4.0 – Predictive Maintenance using Machine Learning")

# ---------------------------------------
# Load Model (SAFE PATH HANDLING)
# ---------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

model = joblib.load(MODEL_PATH)

# ---------------------------------------
# Sidebar Inputs
# ---------------------------------------
st.sidebar.header("🔧 Machine Input Parameters")

machine_type = st.sidebar.selectbox(
    "Machine Type",
    ["L", "M", "H"]
)

air_temp = st.sidebar.number_input(
    "Air Temperature (K)", 290.0, 320.0, 300.0
)

process_temp = st.sidebar.number_input(
    "Process Temperature (K)", 300.0, 350.0, 310.0
)

rot_speed = st.sidebar.number_input(
    "Rotational Speed (rpm)", 1000, 3000, 1500
)

torque = st.sidebar.number_input(
    "Torque (Nm)", 3.0, 80.0, 40.0
)

tool_wear = st.sidebar.number_input(
    "Tool Wear (min)", 0, 250, 100
)

# ---------------------------------------
# Encode Machine Type
# ---------------------------------------
type_mapping = {"L": 0, "M": 1, "H": 2}
machine_type_encoded = type_mapping[machine_type]

# ---------------------------------------
# Create Input Data (ALL TRAINING FEATURES)
# ---------------------------------------
input_dict = {
    "Type": machine_type_encoded,
    "Air temperature [K]": air_temp,
    "Process temperature [K]": process_temp,
    "Rotational speed [rpm]": rot_speed,
    "Torque [Nm]": torque,
    "Tool wear [min]": tool_wear,

    # Failure mode indicators (unknown at prediction time → set to 0)
    "HDF": 0,
    "OSF": 0,
    "PWF": 0,
    "RNF": 0,
    "TWF": 0
}

# Convert to DataFrame
input_data = pd.DataFrame([input_dict])

# ---------------------------------------
# IMPORTANT: Match Training Feature Order
# ---------------------------------------
input_data = input_data[model.feature_names_in_]

# ---------------------------------------
# Prediction
# ---------------------------------------
if st.button("🔍 Predict Machine Status"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.error("⚠️ Machine is likely to FAIL. Schedule maintenance!")
    else:
        st.success("✅ Machine is operating normally.")

    st.info(f"Failure Probability: **{probability:.2%}**")

# ---------------------------------------
# Footer
# ---------------------------------------
st.markdown("---")
st.caption("📊 Predictive Maintenance | ML | Industry 4.0")
