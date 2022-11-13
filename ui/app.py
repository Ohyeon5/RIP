import openai
import streamlit as st
from typing import List, Optional, Callable, Union

from rip.utils import initialize_openai_api, DEFAULT_IMG_URL
from ui.components.input_data import input_data
from ui.components.image_generation import generate_image
from ui.components.text_completion import (
    get_default_completion_params,
    transform_text_to_scene_description,
    get_semantic_search_results,
    get_suggested_actions
)

DEFAULT_COMPLETION_PARAMS = get_default_completion_params()


def init():
    # page settings
    st.set_page_config(
        layout="centered",
        page_title="Reveal Impacts of eco-friendly Policies (RIP)",
        page_icon="eco",
        menu_items={"Get help": "https://github.com/Ohyeon5/RIP"},
    )
    # initialize openai api's variables
    initialize_openai_api()
    # initialize_session_state_keys()


def get_search_question():
    # * Finding resources we can use as an input for our solution. (GPT3 Compare for semantic search and recommendations)
    st.subheader("What solution you are thinking about against lowering CO2 emission?")
    question = st.text_input('What is your favorite solution:', "I'll purchase an electric car")
    return question


def return_search_results(question):
    results = get_semantic_search_results(question)
    # * Grouping, filtering and transforming the inputs which migh be useful for our search on second layer affects of policies and applications. (GPT3 Edit)
    st.subheader("We found those side affects regarding your choice")
    st.write(results)
    actions = get_suggested_actions(question, results)
    return actions



def suggest_actions(actions: str):
    # * Generating quotes and new short definitions from what we found, as a list of takeaways. (GPT3 Explain and Write)
    st.subheader(
        "List of takeaways which might be considered, according to current policies"
    )
    # st.radio(
    #     "Which action best fits?",
    #     actions,
    #     key="action",
    #     # on_change=radio_to_dalle_handler("action"),
    # )
    st.write(actions)
    return actions


def tldr():
    st.subheader("Which impact are you more curious about?")
    text_input = input_data()

    # TODO: enable custome parameter settings
    new_completion_params = DEFAULT_COMPLETION_PARAMS
    # new_completion_params = set_completion_params({"n":2, "best_of":3})
    # new_completion_params = {k: None for k in default_completion_params.keys()}
    # with st.sidebar:
    #     for k, v in default_completion_params.items():
    #         new_completion_params[k] = st.text_input(k, v)

    if text_input:

        text_response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"{text_input} \n\n tl;dr",
            **new_completion_params,
        )
        tldr_text_list = [
            text_response.choices[idx].text for idx in range(len(text_response.choices))
        ]
        tldr_text = st.radio(
            "Which tl;dr best fits ?",
            tldr_text_list,
            key="tldr",
            # on_change=radio_to_dalle_handler("tldr"),
        )
        return tldr_text
    return None


def dalle2(
    text_input: str,
    text_transformer: Optional[Callable] = None,
    button_key: Optional[Union[str, int]] = None,
):
    st.subheader("Your DALL-E representation of the takeaways")
    if text_input:
        if text_transformer:
            text_input = text_transformer(text_input)
        generate_image(text_input=text_input)
    else:
        st.image(DEFAULT_IMG_URL, width=500)
     

if __name__ == "__main__":
    init()
    with st.form(key="seq"):
        question = get_search_question()
        actions = return_search_results(question)
        action = suggest_actions(actions)
        dalle2(action, transform_text_to_scene_description)
        submit1 = st.form_submit_button("DALLE")
    
    # if submit1:
    #     dalle2(action, transform_text_to_scene_description)

    with st.form(key="tldr_res"):    
        tldr_text = tldr()
        submit2 = st.form_submit_button("DALLE")

    if submit2:    
        dalle2(tldr_text, transform_text_to_scene_description)


