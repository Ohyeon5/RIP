import openai
import streamlit as st
import itertools
from typing import Optional, Callable, Union

from rip.utils import initialize_openai_api, DEFAULT_IMG_URL
from ui.components.input_data import input_data
from ui.components.image_generation import generate_image
from ui.components.explore_data import search_relevant_urls
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
        layout="wide",
        page_title="Reveal Impacts of eco-friendly Policies (RIP)",
        page_icon="eco",
        menu_items={"Get help": "https://github.com/Ohyeon5/RIP"},
    )
    # initialize openai api's variables
    initialize_openai_api()


def get_search_question():
    # * Finding resources we can use as an input for our solution. (GPT3 Compare for semantic search and recommendations)
    st.subheader("What solution you are thinking about against lowering CO2 emission?")
    question = st.text_input('What is your favorite solution:', "I'll purchase an electric car")
    return question


def return_search_results(question:str):
    results, keywords = get_semantic_search_results(question)
    # * Grouping, filtering and transforming the inputs which migh be useful for our search on second layer affects of policies and applications. (GPT3 Edit)
    st.subheader("We found those side affects regarding your choice")
    st.write(results)
    st.write(f"Keywords: {keywords}")
    return results, keywords

def suggest_actions(question:str, keywords: str):
    actions = get_suggested_actions(question, keywords)
    # * Generating quotes and new short definitions from what we found, as a list of takeaways. (GPT3 Explain and Write)
    st.subheader(
        "List of takeaways which might be considered"
    )
    st.write(actions)
    return actions

def suggest_urls(keywords: str):
    keywords = list(itertools.chain(*[k.split(sep=' ') for k in keywords.split(sep=',')]))
    title_url_dict = search_relevant_urls(keywords)
    st.subheader(
        "Here are some related policies to have a look :)"
    )
    text = "\n\n ".join([f"[{title}]({url})" for title, url in title_url_dict.items()])
    st.write(text)


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
        )
        return tldr_text
    return None


def dalle2(
    text_input: str,
    text_transformer: Optional[Callable] = None,
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
        _, keywords = return_search_results(question)
        action = suggest_actions(question, keywords)
        suggest_urls(keywords)
        dalle2(action, transform_text_to_scene_description)
        submit1 = st.form_submit_button("DALLE")

    with st.form(key="tldr_res"):    
        tldr_text = tldr()
        dalle2(tldr_text, transform_text_to_scene_description)
        submit2 = st.form_submit_button("DALLE")