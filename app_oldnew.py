import streamlit as st
import time
from ilae_backend import process_clinical_note
import json
import re  # Import the regular expressions module

st.set_page_config(layout="wide")

# Function to display text
def display_text_animated(text):
    st.write(text)

# Function to clean up the ILAE score
def clean_ilae_score(score):
    if isinstance(score, str):
        score_lower = score.lower()
        if 'indeterminate' in score_lower:
            return 'indeterminate'
        else:
            # Try to extract number from the string
            match = re.search(r'\d+', score)
            if match:
                return match.group()
            else:
                return 'Not available'
    elif isinstance(score, int) or isinstance(score, float):
        return str(score)
    else:
        return 'Not available'

# Main app

st.sidebar.title("Upload Clinical Note")
uploaded_file = st.sidebar.file_uploader("Drag and drop your clinical note", type="txt")

uploaded_file_string = uploaded_file.read().decode("utf-8") if uploaded_file else ""

col1, col2 = st.columns([3, 2])

with col1:
    st.title("ILAE Score Calculator")

    if 'score_generated' not in st.session_state:
        st.session_state['score_generated'] = False

    if uploaded_file_string:
        if not st.session_state['score_generated']:
            with st.spinner('Processing...'):
                time.sleep(2)  # Simulate processing delay
                # Call the backend processing function
                final_output, detailed_output = process_clinical_note(uploaded_file_string)
                st.session_state['final_output'] = final_output
                st.session_state['detailed_output'] = detailed_output
                st.session_state['score_generated'] = True  # Set flag to avoid re-processing

        # Extract the ILAE score and explanations from the result
        ilae_score_raw = st.session_state['final_output'].get('ilae_score', "Not available")
        ilae_score = clean_ilae_score(ilae_score_raw)  # Clean up the ILAE score
        concise_explanation = st.session_state['final_output'].get('concise_explanation', "")
        detailed_explanation = st.session_state['detailed_output'].get('detailed_explanation', "")

        st.metric("ILAE Score", ilae_score)

        st.write("---")
        st.subheader("Explanation of the Prediction")

        # Display the concise explanation automatically
        st.write(concise_explanation)

        # Button to show/hide detailed explanation
        if st.button("Show Detailed Explanation"):
            display_text_animated(detailed_explanation)
        else:
            st.write("Press the 'Show Detailed Explanation' button to view the detailed reasoning.")

    else:
        st.write("Please upload a clinical note to calculate the ILAE score.")

with col2:
    if uploaded_file_string:
        st.subheader("Clinical Note")
        st.write(uploaded_file_string)

# Hide Streamlit style
hide_streamlit_style = """
                    <style>
                    div[data-testid="stToolbar"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    div[data-testid="stDecoration"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    div[data-testid="stStatusWidget"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    #MainMenu {
                    visibility: hidden;
                    height: 0%;
                    }
                    header {
                    visibility: hidden;
                    height: 0%;
                    }
                    footer {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    </style>
                    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom styling for the Streamlit app
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F2F6;
    }

    section[data-testid="stSidebar"] {
        background-color: #bacdf2;
    }

    div.stButton > button {
        color: #ffffff;
        background-color: #0072B2;
        border-radius: 5px;
        padding: .5em 1em;
    }

    div.stButton > button:hover {
        background-color: #005282;
        border-color: black;
    }

    h1, h2, h3 {
        color: #395ca0;
    }
    div[data-testid="stMetricValue"] {
        color: #333333 !important;
    }
    p {
        color: #333333;
    }
    section[data-testid="stSidebar"] {
        padding-top: 0rem;
    }
    header {visibility: hidden;}

    div.block-container{padding-top:2rem;}
    </style>
    """,
    unsafe_allow_html=True
)
