import openai
import streamlit as st

from rip.utils import initialize_openai_api, DEFAULT_IMG_URL
from ui.components.input_data import input_initial_data
from rip.utils import get_default_completion_params, set_completion_params


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


def tldr(text_input):

    #* Finding resources we can use as an input for our solution. (GPT3 Compare for semantic search and recommendations)
    st.subheader("What solution you are thinking about against lowering CO2 emission?")
    title = st.text_input('Your favorite solution:', "I'm planning to purchase an electric car")

    #* Grouping, filtering and transforming the inputs which migh be useful for our search on second layer affects of policies and applications. (GPT3 Edit)
    st.subheader("We found those side affects regarding your choice")
    st.write("batteries, aluminium usage, electricity demand, ...")

    #* Generating quotes and new short definitions from what we found, as a list of takeaways. (GPT3 Explain and Write)
    st.subheader("List of takeaways which might be considered, according to current policies")
    st.write("* you can look for the production processes which are using less ... for batteries")
    st.write("* those materials could be picked insted of aluminium usage: ...")
    st.write("* to decrease electricity demand, ...")

    #* Supporting our findings with auto generated images from the copies we generated. (DALL-E)
    st.subheader("Your DALL-E representation of the takeaways")
    st.image(DEFAULT_IMG_URL)

    # TODO: enable custome parameter settings
    default_completion_params = get_default_completion_params()
    new_completion_params = default_completion_params
    # new_completion_params = set_completion_params({"n":2, "best_of":3})
    # new_completion_params = {k: None for k in default_completion_params.keys()}
    # with st.sidebar:
    #     for k, v in default_completion_params.items():
    #         new_completion_params[k] = st.text_input(k, v)

    if st.button("show impact") and text_input:
        
        text_response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"{text_input} \n\n tl;dr", **new_completion_params
        )
        tldr_text_list = [text_response.choices[idx].text for idx in range(len(text_response.choices))]
        tldr_text = st.radio(
            "Which tl;dr best fits ?",
            tldr_text_list)
        if tldr_text:  
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
