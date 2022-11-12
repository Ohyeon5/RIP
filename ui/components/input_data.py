import streamlit as st
from rip.utils import validate_url

def input_initial_data():
    st.write("Which impact are you curious about?")
    type = st.radio(
        "In which format your input is in?",
        ("Text", "PDF file", "URL"),
        horizontal=True,
    )
    text_input = None
    if type == "Text":
        text_input = st.text_input(
            "Input your text",
            placeholder="Add your text here",
        )
    elif type == "PDF file":
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file:
            st.write("upload succeed")
            st.write("But this module is not implemented yet")
            # TODO: use some sort of pdf2json or whatever to convert
    elif type == "URL":
        text_url = st.text_input(
            "Input your url",
            placeholder="Add your url to the text here",
        )
        if text_url:
            st.write("This module is not implemented yet")
            assert validate_url(text_url), "Invalide url"
            # TODO: only get body text from the designated url
    return text_input