import streamlit as st
import time
from ilae_backend import process_clinical_note
import json
import re  # Import the regular expressions module
from difflib import SequenceMatcher  # Import for sequence matching

st.set_page_config(layout="wide")

# Add this near the top of the file, after imports
def reset_session_state():
    st.session_state['score_generated'] = False
    if 'final_output' in st.session_state:
        del st.session_state['final_output']
    if 'detailed_output' in st.session_state:
        del st.session_state['detailed_output']

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

# Helper functions for sentence preprocessing and similarity checking
def preprocess_sentence(s):
    s = s.lower()
    s = re.sub(r'[^\w\s]', '', s)  # Remove punctuation
    s = s.strip()
    return s

def is_similar(a, b, threshold=0.8):
    a_processed = preprocess_sentence(a)
    b_processed = preprocess_sentence(b)
    return SequenceMatcher(None, a_processed, b_processed).ratio() >= threshold

# Main app

st.sidebar.title("Upload Clinical Note")
uploaded_file = st.sidebar.file_uploader("Drag and drop your clinical note", type="txt", 
                                       on_change=reset_session_state)

if uploaded_file is not None:
    uploaded_file_string = uploaded_file.read().decode("utf-8")
else:
    uploaded_file_string = ""

# Adjusted columns
col1, col2, col3 = st.columns([4, 0.1, 5.9])

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

# Replace the col2 section with this updated version
with col2:
    if uploaded_file_string and st.session_state.get('score_generated', False):
        st.markdown(
            '''
            <style>
            .divider {
                border-right: 1px solid #e0e0e0;
                height: calc(100vh - 4rem);
                position: absolute;
                left: 50%;
                margin-top: 1rem;
            }
            </style>
            <div class="divider"></div>
            ''',
            unsafe_allow_html=True
        )

# Move the clinical note display to the third column
with col3:
    if uploaded_file_string:
        st.subheader("Clinical Note")
        
        # Get the extracted entities from the session state
        extracted_entities = st.session_state['final_output'].get('extracted_entities', {})
        clinical_note = uploaded_file_string
        highlighted_text = clinical_note

        # Function to safely highlight text
        def highlight_text(full_text, text_to_highlight):
            if not text_to_highlight or text_to_highlight.lower() == "not found in the clinical note":
                return full_text
            
            # Escape special regex characters in the text to highlight
            escaped_text = re.escape(text_to_highlight)
            
            # Create pattern that matches the text while preserving case
            pattern = re.compile(f'({escaped_text})', re.IGNORECASE)
            
            # Replace with highlighted version
            return pattern.sub(r'<span style="background-color: yellow;">\1</span>', full_text)

        # Highlight all supporting texts from extracted entities
        try:
            for entity, data in extracted_entities.items():
                supporting_text = data.get('supporting_text', '')
                if supporting_text:
                    highlighted_text = highlight_text(highlighted_text, supporting_text)
        
        except Exception as e:
            st.error(f"Error processing highlights: {str(e)}")
        
        # Display the highlighted text
        st.markdown(highlighted_text, unsafe_allow_html=True)

# Hide Streamlit style elements
hide_streamlit_style = """
    <style>
    div[data-testid="stToolbar"] {visibility: hidden; height: 0%; position: fixed;}
    div[data-testid="stDecoration"] {visibility: hidden; height: 0%; position: fixed;}
    div[data-testid="stStatusWidget"] {visibility: hidden; height: 0%; position: fixed;}
    #MainMenu {visibility: hidden; height: 0%;}
    header {visibility: hidden; height: 0%;}
    footer {visibility: hidden; height: 0%; position: fixed;}
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
        background-color: #b3dde8;
        padding-top: 0rem;
    }
    div.stButton > button {
        color: #ffffff;
        background-color: #008bb0;
        border-radius: 5px;
        padding: 0.5em 1em;
    }
    div.stButton > button:hover {
        background-color: #007194;
        border-color: black;
    }
    h1, h2, h3 {
        color: #008bb0;
    }
    div[data-testid="stMetricValue"] {
        color: #333333 !important;
    }
    p {
        color: #333333;
    }
    header {visibility: hidden;}
    div.block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
