import openai
import streamlit as st
from typing import List, Optional, Callable, Union

from rip.utils import initialize_openai_api, DEFAULT_IMG_URL
from ui.components.input_data import input_data
from rip.text_completion import (
    get_default_completion_params,
    set_completion_params,
    transform_text_to_easy_text,
    transform_text_to_scene_description,
)

DEFAULT_COMPLETION_PARAMS = get_default_completion_params()
BUTTON_N=0

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


def get_search_question():
    # * Finding resources we can use as an input for our solution. (GPT3 Compare for semantic search and recommendations)
    st.subheader("What solution you are thinking about against lowering CO2 emission?")
    question = st.text_input('Ask a question about your favorite solution:', "Should I purchase an electric car?")
    return question


def return_search_results(results: List[str]):
    # * Grouping, filtering and transforming the inputs which migh be useful for our search on second layer affects of policies and applications. (GPT3 Edit)
    st.subheader("We found those side affects regarding your choice")
    st.write(", ".join(results))


def suggest_actions(actions: List[str]):
    # * Generating quotes and new short definitions from what we found, as a list of takeaways. (GPT3 Explain and Write)
    st.subheader(
        "List of takeaways which might be considered, according to current policies"
    )
    action = st.radio("Which action best fits?", actions)
    dalle2(action, transform_text_to_scene_description, button_key='action')


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

    if st.button("show impact") and text_input:

        text_response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"{text_input} \n\n tl;dr",
            **new_completion_params,
        )
        tldr_text_list = [
            text_response.choices[idx].text for idx in range(len(text_response.choices))
        ]
        tldr_text = st.radio("Which tl;dr best fits ?", tldr_text_list)
        if tldr_text:
            dalle2(tldr_text, transform_text_to_easy_text, button_key='tldr')

def dalle2(text_input: str, text_transformer: Optional[Callable] = None, button_key: Optional[Union[str, int]]=None):
    st.subheader("Your DALL-E representation of the takeaways")
    if st.button("DALLE", key=button_key) and text_input:
        if text_transformer:
            text_input = text_transformer(text_input)
        img_response = openai.Image.create(prompt=text_input, n=3, size="256x256")
        image_urls = [img_response.data[idx].url for idx in range(len(img_response))]
        st.image(image_urls)
    else:
        st.image(DEFAULT_IMG_URL, width=500)

        
def get_semantic_search_results(question):
    whoami = "I am a highly intelligent question answering bot against lowering CO2 emission. If you comment about your plan for popular eco-friendly solutions, I will answer with the side effects of those."
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=whoami + "\n\nQ: "+ question +"\nA:",
      temperature=0,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n"]
    )
    results = response.choices[0].text.split(sep='.')
    return results

     

if __name__ == "__main__":
    init()
    question = get_search_question()
    #results = ["batteries", "aluminium usage", "electricity demand", "..."]
    results = get_semantic_search_results(question)
    return_search_results(results)
    # TODO: search results to suggested action
    actions = [
        "you can look for the production processes which are using less ... for batteries",
        "those materials could be picked insted of aluminium usage: ...",
        "to decrease electricity demand, ...",
    ]
    suggest_actions(actions)
    tldr()
