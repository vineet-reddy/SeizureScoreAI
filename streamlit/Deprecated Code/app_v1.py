import streamlit as st
from ilae_backend import process_clinical_note

st.title("ILAE Score Calculator")

st.write("""
Upload your clinical note as a `.txt` file, and this app will calculate the ILAE score based on the provided clinical information.
""")

uploaded_file = st.file_uploader("Upload your clinical note (.txt file)", type=["txt"])

if uploaded_file is not None:
    # Read the uploaded file
    clinical_note = uploaded_file.read().decode("utf-8")
    
    st.subheader("Clinical Note")
    st.write(clinical_note)
    
    st.write("Processing...")
    
    # Call the backend processing function
    result = process_clinical_note(clinical_note)
    
    # Display the result
    st.subheader("ILAE Score Calculation Result")
    st.write(result)
