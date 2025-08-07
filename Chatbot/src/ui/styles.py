# src/ui/styles.py
import streamlit as st
from loguru import logger # Import logger directly from loguru

# No need to call get_logger(__name__) here, as loguru.logger is globally configured by setup_logging in app.py

def set_styles():
    """
    Applies custom CSS styles to the Streamlit application for a polished look.
    """
    st.markdown(
        """
        <style>
        /* General body styling */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f2f6;
            color: #333333;
        }

        /* Streamlit main container */
        .stApp {
            background-color: #f0f2f6;
        }

        /* Sidebar styling */
        .st-emotion-cache-1ldf004 { /* Target for the sidebar container */
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }

        /* Header styling */
        h1 {
            color: #4A90E2;
            text-align: center;
            font-weight: 700;
            margin-bottom: 30px;
        }

        h2 {
            color: #333333;
            font-weight: 600;
            margin-top: 25px;
            margin-bottom: 15px;
        }

        /* Chat input and button styling */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #D1D5DB;
            padding: 10px 15px;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);
        }

        .stButton > button {
            background-color: #4A90E2;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .stButton > button:hover {
            background-color: #357ABD;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }

        /* Chat message bubbles */
        .st-emotion-cache-1c7y2kl { /* User message container */
            background-color: #E0F2F7; /* Light blue for user */
            border-radius: 18px 18px 2px 18px;
            padding: 12px 18px;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            align-self: flex-end; /* Align to the right */
        }

        .st-emotion-cache-1m01940 { /* Assistant message container */
            background-color: #FFFFFF; /* White for assistant */
            border-radius: 18px 18px 18px 2px;
            padding: 12px 18px;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            align-self: flex-start; /* Align to the left */
        }

        /* File uploader styling */
        .stFileUploader {
            border: 2px dashed #9BB8D7;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            background-color: #F8F9FA;
        }

        /* Spinner styling */
        .stSpinner > div > div {
            border-top-color: #4A90E2 !important;
        }

        /* Info/Success/Error boxes */
        .stAlert {
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
        }

        .stAlert.info {
            background-color: #E6F7FF;
            border-left: 5px solid #91D5FF;
            color: #0050B3;
        }

        .stAlert.success {
            background-color: #F6FFED;
            border-left: 5px solid #B7EB8F;
            color: #237804;
        }

        .stAlert.error {
            background-color: #FFF1F0;
            border-left: 5px solid #FFA39E;
            color: #A8071A;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
    logger.info("Custom Streamlit styles applied.") # Log style application
