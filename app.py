import requests
import streamlit as st

st.set_page_config(
    page_title="NBA Transaction Tracker",
    page_icon="🏀",
    layout="wide"
)

st.markdown(
    """
    <style>
        .block-container {
            max-width: 900px;
            padding-top: 2rem;
        }
        .stButton>button {
            border-radius: 6px;
            font-weight: 500;
        }
        .ai-box-orange {
            background-color: rgba(255, 85, 0, 0.1) !important;
            border: 1px solid #ff5500 !important;
            color: #ffffff !important;
            padding: 12px 16px;
            border-radius: 8px;
            margin-top: 8px;
            margin-bottom: 8px;
            font-size: 14px;
            line-height: 1.5;
        }
    </style>
    """,
    unsafe_allow_html=True
)
