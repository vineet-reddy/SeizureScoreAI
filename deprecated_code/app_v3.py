import streamlit as st
import time
from ilae_backend import process_clinical_note

st.set_page_config(layout="wide")

# Function to animate text appearing word by word
def display_text_animated(text, delay=0.05):
    words = text.split()
    displayed_text = ""
    placeholder = st.empty()  # Create an empty placeholder for the explanation

    for word in words:
        displayed_text += word + " "
        placeholder.write(displayed_text)  # Update the placeholder with the current text
        time.sleep(delay)  # Wait for the specified delay

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
                result = process_clinical_note(uploaded_file_string)
                st.session_state['result'] = result
                st.session_state['score_generated'] = True  # Set flag to avoid re-processing

        # Extract the ILAE score and explanation from the result
        ilae_score = "Not available"
        explanation_text = st.session_state['result']

        # Attempt to extract the ILAE score from the result
        # Assuming the ILAE score is mentioned in a consistent format like "Class X"
        import re
        match = re.search(r'Class (\d)', explanation_text)
        if match:
            ilae_score = f"Class {match.group(1)}"

        st.metric("ILAE Score", ilae_score)

        st.write("---")
        st.subheader("Explanation of the Prediction")

        # Button to trigger explanation animation
        if st.button("Show Explanation"):
            display_text_animated(explanation_text)
        else:
            st.write("Press the 'Show Explanation' button to view the detailed reasoning.")

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
