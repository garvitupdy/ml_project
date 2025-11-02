import streamlit as st
import pandas as pd
import numpy as np
import joblib


# Page configuration
st.set_page_config(
    page_title="Stroke Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 18px;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
    }
    .high-risk {
        background-color: #ffcccc;
        color: #cc0000;
        border: 3px solid #cc0000;
    }
    .low-risk {
        background-color: #ccffcc;
        color: #006600;
        border: 3px solid #006600;
    }
    </style>
""", unsafe_allow_html=True)

model = joblib.load("model.pkl")

expected_columns = joblib.load("columns.pkl")

# Header
st.markdown('<p class="main-header">🏥 Stroke Risk Prediction System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Early detection can save lives. Please answer the following questions honestly.</p>', unsafe_allow_html=True)

st.markdown("---")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Basic Information")
    
    # Age input
    Age = st.number_input(
        "What is your age?",
        min_value=1,
        max_value=120,
        value=30,
        step=1,
        help="Enter your age in years"
    )
    
    st.markdown("---")
    st.subheader("🩺 General Symptoms")
    
    # Anxiety
    Anxiety = st.radio(
        "Are you feeling anxious?",
        options=["No", "Yes"],
        index=0,
        help="Select if you're experiencing anxiety"
    )
    
    # Excessive sweating
    Sweating = st.radio(
        "Are you sweating more than usual?",
        options=["No", "Yes"],
        index=0,
        help="Select if you're experiencing excessive sweating"
    )
    
    # Swelling
    Swelling = st.radio(
        "Is any body part swollen out of nowhere?",
        options=["No", "Yes"],
        index=0,
        help="Select if you're experiencing unexplained swelling"
    )
    
    # Fatigue
    Fatigue = st.radio(
        "Are you feeling tired without doing physically demanding activities?",
        options=["No", "Yes"],
        index=0,
        help="Select if you're experiencing unusual fatigue"
    )

with col2:
    st.subheader("❤️ Cardiovascular Symptoms")
    
    cardio_systems = st.radio(
        "Are you experiencing any of these: chest pain, chest discomfort, irregular heartbeat, or high blood pressure?",
        options=[
            "I am not feeling any of these",
            "I am feeling one of these symptoms",
            "I am feeling two of these symptoms",
            "I am feeling three of these symptoms",
            "I am feeling four of these symptoms"
        ],
        index=0,
        help="Select the number of cardiovascular symptoms you're experiencing"
    )
    
    st.markdown("---")
    st.subheader("🧠 Neurological Symptoms")
    
    neuro_systems = st.radio(
        "Are you experiencing any of these: dizziness, cervical discomfort, cold limbs, or vomiting?",
        options=[
            "I am not feeling any of these",
            "I am feeling one of these symptoms",
            "I am feeling two of these symptoms",
            "I am feeling three of these symptoms",
            "I am feeling four of these symptoms"
        ],
        index=0,
        help="Select the number of neurological symptoms you're experiencing"
    )
    
    st.markdown("---")
    st.subheader("🫁 Respiratory Symptoms")
    
    respiratory = st.radio(
        "Are you experiencing any of these: shortness of breath, snoring, or persistent cough?",
        options=[
            "I am not feeling any of these",
            "I am feeling one of these symptoms",
            "I am feeling two of these symptoms",
            "I am feeling three of these symptoms"
        ],
        index=0,
        help="Select the number of respiratory symptoms you're experiencing"
    )

st.markdown("---")

# Convert inputs to model format
def convert_yes_no(value):
    return 1 if value == "Yes" else 0

def convert_symptoms_count(value):
    mapping = {
        "I am not feeling any of these": 0,
        "I am feeling one of these symptoms": 1,
        "I am feeling two of these symptoms": 2,
        "I am feeling three of these symptoms": 3,
        "I am feeling four of these symptoms": 4
    }
    return mapping.get(value, 0)

# Predict button
predict_button = st.button("🔍 Predict Stroke Risk")



if predict_button:
    # Prepare input data
    input_data = {
        'age': Age,
        'anxiety': convert_yes_no(Anxiety),
        'excessive_sweating': convert_yes_no(Sweating),
        'swelling': convert_yes_no(Swelling),
        'fatigue': convert_yes_no(Fatigue),
        'cardio_systems': convert_symptoms_count(cardio_systems),
        'neuro_systems': convert_symptoms_count(neuro_systems),
        'respiratiory': convert_symptoms_count(respiratory)  # Note: keeping your spelling 'respiratiory'
    }
    
    # Create DataFrame
    input_df = pd.DataFrame([input_data])

    

    

    
    # Display input summary
    with st.expander("📊 View Your Input Summary"):
        st.dataframe(input_df, use_container_width=True)
    
    # Make prediction (uncomment when model is ready)
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0]
    
    # Dummy prediction for demonstration (remove when model is ready)
    prediction = np.random.choice([0, 1])  # Replace with actual model prediction
    prediction_proba = [0.7, 0.3] if prediction == 0 else [0.3, 0.7]  # Replace with actual probabilities
    
    st.markdown("---")
    st.subheader("🎯 Prediction Results")
    
    if prediction == 1:
        st.markdown(
            '<div class="prediction-box high-risk">⚠️ HIGH RISK: Stroke Risk Detected</div>',
            unsafe_allow_html=True
        )
        st.error("**Important:** The model indicates a potential stroke risk. Please consult a healthcare professional immediately!")
        st.write(f"**Confidence:** {prediction_proba[1]*100:.2f}%")
        
        st.markdown("### 🚨 Recommended Actions:")
        st.markdown("""
        - **Seek immediate medical attention**
        - Call emergency services if experiencing severe symptoms
        - Do not ignore warning signs
        - Keep a record of your symptoms
        - Inform family members or caregivers
        """)
        
    else:
        st.markdown(
            '<div class="prediction-box low-risk">✅ LOW RISK: No Immediate Stroke Risk Detected</div>',
            unsafe_allow_html=True
        )
        st.success("**Good News:** The model indicates a lower stroke risk based on your inputs.")
        st.write(f"**Confidence:** {prediction_proba[0]*100:.2f}%")
        
        st.markdown("### 💡 Preventive Measures:")
        st.markdown("""
        - Maintain a healthy lifestyle
        - Regular exercise and balanced diet
        - Monitor blood pressure regularly
        - Avoid smoking and excessive alcohol
        - Schedule regular health check-ups
        """)
    
    st.markdown("---")
    st.info("⚕️ **Disclaimer:** This prediction is based on a machine learning model and should not replace professional medical advice. Always consult with a healthcare provider for proper diagnosis and treatment.")

# Sidebar information
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/heart-with-pulse.png", width=100)
    st.title("About")
    st.info("""
    This Stroke Prediction System uses machine learning to assess stroke risk based on various symptoms and factors.
    
    **How it works:**
    1. Answer all questions honestly
    2. Click 'Predict Stroke Risk'
    3. Review your results
    4. Follow recommended actions
    
    **Remember:** Early detection is key to prevention!
    """)
    
    st.markdown("---")
    st.subheader("⚠️ Warning Signs of Stroke")
    st.markdown("""
    **F.A.S.T:**
    - **F**ace drooping
    - **A**rm weakness
    - **S**peech difficulty
    - **T**ime to call emergency
    
    If you experience these, call emergency services immediately!
    """)
    
    st.markdown("---")
    st.caption("🏥 Stroke Prediction System v1.0")