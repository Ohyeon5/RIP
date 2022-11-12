import openai
import streamlit as st

from rip.utils import initialize_openai_api, DEFAULT_IMG_URL, validate_url
from ui.components.input_data import input_initial_data


def init():
    # page settings
    st.set_page_config(
        layout="centered",
        page_title="Reveal Impacts of eco-friendly Policies (RIP)",
        page_icon="globe",
        menu_items={"Get help": "https://github.com/Ohyeon5/RIP"},
    )
    # initialize openai api's variables
    initialize_openai_api()


def tldr(text_input):

    # TODO: enable custome parameter settings
    # TODO: enable multiple tl;dr outputs

    if st.button("show impact") and text_input:
        text_response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"{text_input} \n\n tl;dr",
            temperature=0.7,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        tldr_text = text_response.choices[0].text
        st.write(tldr_text)
        return tldr_text
    else:
        return None


def dalle2(text_input):
    if text_input:
        img_response = openai.Image.create(prompt=text_input, n=1, size="1024x1024")
        image_url = img_response.data[0].url
        st.image(image_url)
    else:
        st.image(DEFAULT_IMG_URL, width=500)


if __name__ == "__main__":
    init()
    text_input = input_initial_data()
    text = tldr(text_input)
    dalle2(text)
