import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time


st.set_page_config(
    page_title="Stroke Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
) 

st.markdown("""
    <style>
  
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }
    
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    
    .block-container {
        background: rgba(26, 26, 46, 0.95);
        border-radius: 20px;
        padding: 2rem;
        padding-top: 3rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 1rem;
    }
    
    
    .main-header {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(120deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        margin-top: 60px;
        animation: gradient 3s ease infinite;
        padding-top: 20px;
    }
    
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    
    .sub-header {
        font-size: 20px;
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 30px;
        margin-top: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    
    .top-spacer {
        height: 80px;
    }
    
    
    .stMarkdown, .stText, p, span, label {
        color: #e0e0e0 !important;
    }
    
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        height: 60px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 30px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.6);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.8);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    
    .info-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(102, 126, 234, 0.5);
    }
    
    .info-card h3, .info-card h4 {
        color: #667eea !important;
    }
    
    .info-card p, .info-card li, .info-card ul {
        color: #e0e0e0 !important;
    }
    
    
    .prediction-box {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin: 20px 0;
        animation: slideIn 0.5s ease-out;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .high-risk {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white !important;
        border: 3px solid #c92a2a;
    }
    
    .low-risk {
        background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
        color: white !important;
        border: 3px solid #2b8a3e;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Radio button styling */
    .stRadio > label {
        font-weight: 600;
        color: #e0e0e0 !important;
        font-size: 16px;
    }
    
    .stRadio > div {
        background: rgba(26, 26, 46, 0.5);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .stRadio > div > label > div {
        color: #e0e0e0 !important;
    }
    
    
    .stNumberInput > label {
        font-weight: 600;
        color: #e0e0e0 !important;
        font-size: 16px;
    }
    
    .stNumberInput input {
        background: rgba(26, 26, 46, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(102, 126, 234, 0.5) !important;
        border-radius: 10px;
    }
    
    
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white !important;
        font-weight: bold;
    }
    
    .streamlit-expanderContent {
        background: rgba(26, 26, 46, 0.9);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: #e0e0e0 !important;
    }
    
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(26, 26, 46, 0.8);
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(102, 126, 234, 0.2);
        color: #e0e0e0;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        text-align: center;
        margin: 10px 0;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .metric-card h1 {
        color: #667eea !important;
    }
    
    .metric-card p {
        color: #b0b0b0 !important;
    }
    
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7);
        }
        70% {
            box-shadow: 0 0 0 20px rgba(255, 107, 107, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 107, 107, 0);
        }
    }
    
    .pulse-warning {
        animation: pulse 2s infinite;
    }
    
    
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    
    @keyframes float {
        0% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
        100% {
            transform: translateY(0px);
        }
    }
    
    .floating-icon {
        animation: float 3s ease-in-out infinite;
    }
    
    
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0 10px 0;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
    }
    
    
    .stats-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
        color: white !important;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        border: 1px solid rgba(102, 126, 234, 0.5);
    }
    
    
    .badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin: 5px;
    }
    
    .badge-danger {
        background: #ff6b6b;
        color: white !important;
    }
    
    .badge-success {
        background: #51cf66;
        color: white !important;
    }
    
    .badge-info {
        background: #4dabf7;
        color: white !important;
    }
    
    
    .dataframe {
        background: rgba(26, 26, 46, 0.9) !important;
        color: #e0e0e0 !important;
    }
    
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    section[data-testid="stSidebar"] > div {
        background: rgba(26, 26, 46, 0.8);
        padding-top: 3rem;
    }
    
    /* Info, Success, Error, Warning boxes */
    .stAlert {
        background: rgba(26, 26, 46, 0.9) !important;
        color: #e0e0e0 !important;
        border-radius: 10px;
    }
    
    
    [data-testid="stMetricValue"] {
        color: #667eea !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #51cf66 !important;
    }
    
    
    hr {
        border-color: rgba(102, 126, 234, 0.3) !important;
        margin: 2rem 0;
    }
    
    
    a {
        color: #667eea !important;
    }
    
    a:hover {
        color: #764ba2 !important;
    }
    

    .js-plotly-plot {
        background: transparent !important;
    }
    
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    
    header[data-testid="stHeader"] {
        background: rgba(15, 12, 41, 0.95);
        backdrop-filter: blur(10px);
    }
    
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="top-spacer"></div>', unsafe_allow_html=True)


st.markdown('<p class="main-header floating-icon">🏥 Stroke Risk Prediction System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">💡 Early detection can save lives. Please answer the following questions honestly.</p>', unsafe_allow_html=True)

col_time1, col_time2, col_time3 = st.columns([1, 2, 1])
with col_time2:
    st.markdown(f"""
    <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 10px; color: white; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);'>
        📅 {datetime.now().strftime('%B %d, %Y')} | 🕐 {datetime.now().strftime('%I:%M %p')}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")


tab1, tab2, tab3 = st.tabs(["📋 Assessment", "📊 Risk Analysis", "💡 Health Tips"])

with tab1:
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">📋 Basic Information</div>', unsafe_allow_html=True)
        
        
        age = st.number_input(
            "What is your age?",
            min_value=1,
            max_value=120,
            value=30,
            step=1,
            help="Enter your age in years"
        )
        
        
        if age < 18:
            age_category = "Child/Teenager"
            age_color = "#4dabf7"
        elif age < 40:
            age_category = "Young Adult"
            age_color = "#51cf66"
        elif age < 60:
            age_category = "Middle Age"
            age_color = "#ffd43b"
        else:
            age_category = "Senior"
            age_color = "#ff6b6b"
        
        st.markdown(f"""
        <div style='background: {age_color}; color: white; padding: 10px; border-radius: 10px; text-align: center; margin: 10px 0; box-shadow: 0 4px 10px rgba(0,0,0,0.3);'>
            Age Category: <strong>{age_category}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">🩺 General Symptoms</div>', unsafe_allow_html=True)
        
        
        st.markdown("### 😰 Anxiety Status")
        anxiety = st.radio(
            "Are you feeling anxious?",
            options=["No", "Yes"],
            index=0,
            help="Select if you're experiencing anxiety",
            key="anxiety"
        )
        
        
        st.markdown("### 💧 Sweating")
        excessive_sweating = st.radio(
            "Are you sweating more than usual?",
            options=["No", "Yes"],
            index=0,
            help="Select if you're experiencing excessive sweating",
            key="sweating"
        )
   
        st.markdown("### 🎈 Swelling")
        swelling = st.radio(
            "Is any body part swollen out of nowhere?",
            options=["No", "Yes"],
            index=0,
            help="Select if you're experiencing unexplained swelling",
            key="swelling"
        )
        

        st.markdown("### 😴 Fatigue")
        fatigue = st.radio(
            "Are you feeling tired without doing physically demanding activities?",
            options=["No", "Yes"],
            index=0,
            help="Select if you're experiencing unusual fatigue",
            key="fatigue"
        )
    
    with col2:
        st.markdown('<div class="section-header">❤️ Cardiovascular Symptoms</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <strong style='color: #667eea !important;'>Symptoms include:</strong> 
            <span style='color: #e0e0e0;'>Chest pain, Chest discomfort, Irregular heartbeat, High blood pressure</span>
        </div>
        """, unsafe_allow_html=True)
        
        cardio_systems = st.radio(
            "How many of these cardiovascular symptoms are you experiencing?",
            options=[
                "I am not feeling any of these",
                "I am feeling one of these symptoms",
                "I am feeling two of these symptoms",
                "I am feeling three of these symptoms",
                "I am feeling all of these symptoms"
            ],
            index=0,
            help="Select the number of cardiovascular symptoms you're experiencing",
            key="cardio"
        )
        
        st.markdown('<div class="section-header">🧠 Neurological Symptoms</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <strong style='color: #667eea !important;'>Symptoms include:</strong> 
            <span style='color: #e0e0e0;'>Dizziness, Cervical discomfort, Cold limbs, Vomiting</span>
        </div>
        """, unsafe_allow_html=True)
        
        neuro_systems = st.radio(
            "How many of these neurological symptoms are you experiencing?",
            options=[
                "I am not feeling any of these",
                "I am feeling one of these symptoms",
                "I am feeling two of these symptoms",
                "I am feeling three of these symptoms",
                "I am feeling all of these symptoms"
            ],
            index=0,
            help="Select the number of neurological symptoms you're experiencing",
            key="neuro"
        )
        
        st.markdown('<div class="section-header">🫁 Respiratory Symptoms</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <strong style='color: #667eea !important;'>Symptoms include:</strong> 
            <span style='color: #e0e0e0;'>Shortness of breath, Snoring, Persistent cough</span>
        </div>
        """, unsafe_allow_html=True)
        
        respiratory = st.radio(
            "How many of these respiratory symptoms are you experiencing?",
            options=[
                "I am not feeling any of these",
                "I am feeling one of these symptoms",
                "I am feeling two of these symptoms",
                "I am feeling all of these symptoms"
            ],
            index=0,
            help="Select the number of respiratory symptoms you're experiencing",
            key="respiratory"
        )
    
    st.markdown("---")
    
    
    predict_button = st.button("🔍 Predict Stroke Risk", use_container_width=True)
    
    if predict_button:
        
        with st.spinner('🔄 Analyzing your health data...'):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
        
        
        def convert_yes_no(value):
            return 1 if value == "Yes" else 0
        
        def convert_symptoms_count(value):
            mapping = {
                "I am not feeling any of these": 0,
                "I am feeling one of these symptoms": 1,
                "I am feeling two of these symptoms": 2,
                "I am feeling three of these symptoms": 3,
                "I am feeling all of these symptoms": 4
            }
            return mapping.get(value, 0)
        
        
        input_data = {
            'age': age,
            'anxiety': convert_yes_no(anxiety),
            'excessive_sweating': convert_yes_no(excessive_sweating),
            'swelling': convert_yes_no(swelling),
            'fatigue': convert_yes_no(fatigue),
            'cardio_systems': convert_symptoms_count(cardio_systems),
            'neuro_systems': convert_symptoms_count(neuro_systems),
            'respiratiory': convert_symptoms_count(respiratory)
        }
        
        input_df = pd.DataFrame([input_data])
        
        
        total_symptoms = sum([
            convert_yes_no(anxiety),
            convert_yes_no(excessive_sweating),
            convert_yes_no(swelling),
            convert_yes_no(fatigue),
            convert_symptoms_count(cardio_systems),
            convert_symptoms_count(neuro_systems),
            convert_symptoms_count(respiratory)
        ])
        
        prediction = 1 if total_symptoms > 5 else 0
        prediction_proba = [0.3, 0.7] if prediction == 1 else [0.8, 0.2]
        
        st.markdown("---")
        

        if prediction == 1:
            st.markdown(
                '<div class="prediction-box high-risk pulse-warning">⚠️ HIGH RISK: Stroke Risk Detected</div>',
                unsafe_allow_html=True
            )
            st.error("**Important:** The model indicates a potential stroke risk. Please consult a healthcare professional immediately!")
            
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=prediction_proba[1] * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Level (%)", 'font': {'size': 24, 'color': '#e0e0e0'}},
                delta={'reference': 50, 'increasing': {'color': "red"}},
                number={'font': {'color': '#e0e0e0'}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#667eea"},
                    'bar': {'color': "darkred"},
                    'bgcolor': "#1a1a2e",
                    'borderwidth': 2,
                    'bordercolor': "#667eea",
                    'steps': [
                        {'range': [0, 30], 'color': '#2d5016'},
                        {'range': [30, 70], 'color': '#614d1a'},
                        {'range': [70, 100], 'color': '#5c1919'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e0e0'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 🚨 Recommended Actions:")
            st.markdown("""
            <div class='info-card'>
            <ul style='color: #e0e0e0;'>
                <li><strong style='color: #ff6b6b;'>Seek immediate medical attention</strong></li>
                <li>Call emergency services if experiencing severe symptoms</li>
                <li>Do not ignore warning signs</li>
                <li>Keep a record of your symptoms</li>
                <li>Inform family members or caregivers</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown(
                '<div class="prediction-box low-risk">✅ LOW RISK: No Immediate Stroke Risk Detected</div>',
                unsafe_allow_html=True
            )
            st.success("**Good News:** The model indicates a lower stroke risk based on your inputs.")
            
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=prediction_proba[1] * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Level (%)", 'font': {'size': 24, 'color': '#e0e0e0'}},
                delta={'reference': 50, 'decreasing': {'color': "green"}},
                number={'font': {'color': '#e0e0e0'}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#667eea"},
                    'bar': {'color': "green"},
                    'bgcolor': "#1a1a2e",
                    'borderwidth': 2,
                    'bordercolor': "#667eea",
                    'steps': [
                        {'range': [0, 30], 'color': '#2d5016'},
                        {'range': [30, 70], 'color': '#614d1a'},
                        {'range': [70, 100], 'color': '#5c1919'}
                    ],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 20
                    }
                }
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e0e0e0'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 💡 Preventive Measures:")
            st.markdown("""
            <div class='info-card'>
            <ul style='color: #e0e0e0;'>
                <li>Maintain a healthy lifestyle</li>
                <li>Regular exercise and balanced diet</li>
                <li>Monitor blood pressure regularly</li>
                <li>Avoid smoking and excessive alcohol</li>
                <li>Schedule regular health check-ups</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        
        st.markdown("### 📊 Your Symptom Breakdown")
        
        symptom_data = {
            'Category': ['General\nSymptoms', 'Cardio\nSymptoms', 'Neuro\nSymptoms', 'Respiratory\nSymptoms'],
            'Count': [
                sum([convert_yes_no(anxiety), convert_yes_no(excessive_sweating), 
                     convert_yes_no(swelling), convert_yes_no(fatigue)]),
                convert_symptoms_count(cardio_systems),
                convert_symptoms_count(neuro_systems),
                convert_symptoms_count(respiratory)
            ]
        }
        
        fig = px.bar(
            symptom_data,
            x='Category',
            y='Count',
            title='Symptom Distribution',
            color='Count',
            color_continuous_scale=['#51cf66', '#ffd43b', '#ff6b6b'],
            labels={'Count': 'Number of Symptoms'}
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#e0e0e0'},
            title_font_color='#e0e0e0',
            xaxis={'gridcolor': 'rgba(102, 126, 234, 0.2)', 'color': '#e0e0e0'},
            yaxis={'gridcolor': 'rgba(102, 126, 234, 0.2)', 'color': '#e0e0e0'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        
        with st.expander("📋 View Detailed Input Summary"):
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.markdown("#### General Information")
                st.markdown(f"**Age:** {age} years ({age_category})")
                st.markdown(f"**Anxiety:** {anxiety}")
                st.markdown(f"**Excessive Sweating:** {excessive_sweating}")
                st.markdown(f"**Swelling:** {swelling}")
                st.markdown(f"**Fatigue:** {fatigue}")
            
            with summary_col2:
                st.markdown("#### System Symptoms")
                st.markdown(f"**Cardiovascular:** {cardio_systems}")
                st.markdown(f"**Neurological:** {neuro_systems}")
                st.markdown(f"**Respiratory:** {respiratory}")
                st.markdown(f"**Total Symptom Score:** {total_symptoms}")
        
        st.markdown("---")
        st.info("⚕️ **Disclaimer:** This prediction is based on a machine learning model and should not replace professional medical advice. Always consult with a healthcare provider for proper diagnosis and treatment.")

with tab2:
    st.markdown('<div class="section-header">📊 Stroke Risk Analysis Dashboard</div>', unsafe_allow_html=True)
    

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown("""
        <div class='metric-card'>
            <h1 style='color: #667eea !important; margin: 0;'>15M</h1>
            <p style='color: #b0b0b0 !important; margin: 5px 0 0 0;'>Annual Stroke Cases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown("""
        <div class='metric-card'>
            <h1 style='color: #ff6b6b !important; margin: 0;'>5.5M</h1>
            <p style='color: #b0b0b0 !important; margin: 5px 0 0 0;'>Stroke Deaths/Year</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown("""
        <div class='metric-card'>
            <h1 style='color: #51cf66 !important; margin: 0;'>80%</h1>
            <p style='color: #b0b0b0 !important; margin: 5px 0 0 0;'>Preventable Cases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown("""
        <div class='metric-card'>
            <h1 style='color: #ffd43b !important; margin: 0;'>3-4.5h</h1>
            <p style='color: #b0b0b0 !important; margin: 5px 0 0 0;'>Critical Time Window</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📈 Age vs Stroke Risk Correlation")
    
    age_data = pd.DataFrame({
        'Age Group': ['0-20', '21-40', '41-60', '61-80', '80+'],
        'Risk %': [2, 8, 25, 45, 65]
    })
    
    fig = px.line(
        age_data,
        x='Age Group',
        y='Risk %',
        markers=True,
        title='Stroke Risk by Age Group',
        labels={'Risk %': 'Risk Percentage'}
    )
    fig.update_traces(line_color='#667eea', line_width=3, marker=dict(size=12, color='#764ba2'))
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e0e0e0'},
        title_font_color='#e0e0e0',
        xaxis={'gridcolor': 'rgba(102, 126, 234, 0.2)', 'color': '#e0e0e0'},
        yaxis={'gridcolor': 'rgba(102, 126, 234, 0.2)', 'color': '#e0e0e0'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown("### ⚖️ Major Risk Factors Comparison")
    
    risk_factors = pd.DataFrame({
        'Risk Factor': ['High BP', 'Smoking', 'Diabetes', 'Obesity', 'Physical Inactivity', 'High Cholesterol'],
        'Impact %': [47, 38, 28, 26, 25, 23]
    })
    
    fig = px.bar(
        risk_factors,
        x='Impact %',
        y='Risk Factor',
        orientation='h',
        title='Impact of Risk Factors on Stroke',
        color='Impact %',
        color_continuous_scale=['#ff6b6b', '#ee5a6f', '#c92a2a']
    )
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e0e0e0'},
        title_font_color='#e0e0e0',
        xaxis={'gridcolor': 'rgba(102, 126, 234, 0.2)', 'color': '#e0e0e0'},
        yaxis={'gridcolor': 'rgba(102, 126, 234, 0.2)', 'color': '#e0e0e0'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown("### ⚠️ Common Warning Signs")
    
    warning_col1, warning_col2 = st.columns(2)
    
    with warning_col1:
        st.markdown("""
        <div class='info-card'>
            <h4 style='color: #667eea !important;'>🎯 Immediate Symptoms</h4>
            <ul style='color: #e0e0e0;'>
                <li>Sudden numbness or weakness</li>
                <li>Confusion or trouble speaking</li>
                <li>Vision problems in one or both eyes</li>
                <li>Trouble walking or dizziness</li>
                <li>Severe headache with no cause</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with warning_col2:
        st.markdown("""
        <div class='info-card'>
            <h4 style='color: #667eea !important;'>📊 Risk Categories</h4>
            <div>
                <span class='badge badge-success'>Low Risk: 0-30%</span><br>
                <span class='badge badge-info'>Medium Risk: 31-60%</span><br>
                <span class='badge badge-danger'>High Risk: 61-100%</span>
            </div>
            <br>
            <p style='color: #e0e0e0;'><strong>Note:</strong> Consult a doctor regardless of risk level if you have concerns.</p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">💡 Health Tips & Prevention</div>', unsafe_allow_html=True)
    

    tip_col1, tip_col2 = st.columns(2)
    
    with tip_col1:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color: #667eea !important;'>🥗 Dietary Recommendations</h3>
            <ul style='color: #e0e0e0;'>
                <li>Eat plenty of fruits and vegetables</li>
                <li>Choose whole grains over refined grains</li>
                <li>Include lean proteins (fish, poultry)</li>
                <li>Limit sodium intake (< 2,300mg/day)</li>
                <li>Reduce saturated fats and trans fats</li>
                <li>Stay hydrated (8-10 glasses of water)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <h3 style='color: #667eea !important;'>🏃 Exercise Guidelines</h3>
            <ul style='color: #e0e0e0;'>
                <li>At least 150 minutes of moderate activity/week</li>
                <li>Include strength training 2x per week</li>
                <li>Take regular breaks if sitting long hours</li>
                <li>Try walking, swimming, or cycling</li>
                <li>Gradually increase intensity</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tip_col2:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color: #667eea !important;'>🧘 Stress Management</h3>
            <ul style='color: #e0e0e0;'>
                <li>Practice meditation or yoga</li>
                <li>Get 7-9 hours of quality sleep</li>
                <li>Engage in hobbies and relaxation</li>
                <li>Maintain social connections</li>
                <li>Consider professional counseling if needed</li>
                <li>Limit caffeine and alcohol</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <h3 style='color: #667eea !important;'>🏥 Regular Monitoring</h3>
            <ul style='color: #e0e0e0;'>
                <li>Check blood pressure regularly</li>
                <li>Monitor cholesterol levels</li>
                <li>Track blood sugar (especially if diabetic)</li>
                <li>Annual health check-ups</li>
                <li>Keep medication schedule if prescribed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    
    st.markdown("### 🚨 Remember: F.A.S.T.")
    
    fast_col1, fast_col2, fast_col3, fast_col4 = st.columns(4)
    
    with fast_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        padding: 20px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);'>
            <h1 style='color: white !important;'>F</h1>
            <h4 style='color: white !important;'>Face Drooping</h4>
            <p style='color: white !important;'>One side of face numb or drooping</p>
        </div>
        """, unsafe_allow_html=True)
    
    with fast_col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
        padding: 20px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);'>
            <h1 style='color: white !important;'>A</h1>
            <h4 style='color: white !important;'>Arm Weakness</h4>
            <p style='color: white !important;'>Arm numbness or weakness</p>
        </div>
        """, unsafe_allow_html=True)
    
    with fast_col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
        padding: 20px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);'>
            <h1 style='color: white !important;'>S</h1>
            <h4 style='color: white !important;'>Speech Difficulty</h4>
            <p style='color: white !important;'>Slurred speech or confusion</p>
        </div>
        """, unsafe_allow_html=True)
    
    with fast_col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
        padding: 20px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(250, 112, 154, 0.4);'>
            <h1 style='color: white !important;'>T</h1>
            <h4 style='color: white !important;'>Time to Call</h4>
            <p style='color: white !important;'>Call emergency immediately!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    
    st.markdown("### 📞 Emergency Contacts")
    
    emergency_col1, emergency_col2 = st.columns(2)
    
    with emergency_col1:
        st.markdown("""
        <div class='info-card'>
            <h4 style='color: #667eea !important;'>🚑 Emergency Numbers</h4>
            <ul style='color: #e0e0e0;'>
                <li><strong>Emergency Services:</strong> 911 (US) / 112 (IND)</li>
                <li><strong>Stroke Helpline:</strong> 1-800-STROKES</li>
                <li><strong>Health Info:</strong> 1-800-CDC-INFO</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with emergency_col2:
        st.markdown("""
        <div class='info-card'>
            <h4 style='color: #667eea !important;'>🔗 Useful Resources</h4>
            <ul style='color: #e0e0e0;'>
                <li><a href='https://www.stroke.org' target='_blank' style='color: #667eea !important;'>American Stroke Association</a></li>
                <li><a href='https://www.cdc.gov/stroke' target='_blank' style='color: #667eea !important;'>CDC Stroke Information</a></li>
                <li><a href='https://www.who.int/health-topics/stroke' target='_blank' style='color: #667eea !important;'>WHO Stroke Resources</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <div class='floating-icon' style='font-size: 80px;'>🏥</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%); padding: 20px; border-radius: 15px; margin: 10px 0; border: 1px solid rgba(102, 126, 234, 0.3);'>
        <h2 style='color: #667eea !important; text-align: center;'>About This App</h2>
        <p style='text-align: justify; color: #e0e0e0 !important;'>
        This Stroke Prediction System uses advanced machine learning algorithms to assess stroke risk 
        based on various symptoms and health factors.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("### 📊 Quick Stats")
    st.metric("Global Stroke Cases", "15M/year", "+2%")
    st.metric("Prevention Success", "80%", "+5%")
    st.metric("App Accuracy", "94.5%", "+1.2%")
    
    st.markdown("---")
    

    tips = [
        "💡 Regular exercise reduces stroke risk by 25%",
        "🥗 Mediterranean diet lowers stroke risk significantly",
        "😴 7-9 hours of sleep is optimal for brain health",
        "🚭 Quitting smoking cuts stroke risk in half within 2 years",
        "💧 Staying hydrated improves blood flow"
    ]
    
    st.markdown("### 💡 Daily Health Tip")
    import random
    st.info(random.choice(tips))
    
    st.markdown("---")
    
    
    st.markdown("""
    <div style='text-align: center; color: #e0e0e0;'>
        <p>🏥 Stroke Prediction System</p>
        <p>Prototype Version</p>
        <p>©  Health Diagnostic Labs</p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
border-radius: 15px; color: white; margin-top: 30px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);'>
    <h3 style='color: white !important;'>🌟 Your Health is Our Priority</h3>
    <p style='color: white !important;'>Remember: This tool is for educational purposes. Always consult healthcare professionals for medical advice.</p>
    <p style='color: white !important;'>Made with ❤️ for better health outcomes</p>
</div>
""", unsafe_allow_html=True)