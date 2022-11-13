import openai
import streamlit as st
from typing import List

from rip.utils import initialize_openai_api, DEFAULT_IMG_URL
from ui.components.input_data import input_data
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

def get_search_question():
    #* Finding resources we can use as an input for our solution. (GPT3 Compare for semantic search and recommendations)
    st.subheader("What solution you are thinking about against lowering CO2 emission?")
    question = st.text_input('What is your favorite solution:', "I'll purchase an electric car")
    return question

def return_search_results(results: List[str]):
    #* Grouping, filtering and transforming the inputs which migh be useful for our search on second layer affects of policies and applications. (GPT3 Edit)
    st.subheader("We found those side affects regarding your choice")
    st.write(", ".join(results))

def suggest_actions(actions: List[str]):
    #* Generating quotes and new short definitions from what we found, as a list of takeaways. (GPT3 Explain and Write)
    st.subheader("List of takeaways which might be considered, according to current policies")
    action = st.radio(
            "Which action best fits?",
            actions)
    dalle2(action)
  
    
def tldr():     
    st.subheader("Which impact are you more curious about?")
    text_input = input_data()

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
            dalle2(tldr_text)


def dalle2(text_input):
    st.subheader("Your DALL-E representation of the takeaways")
    if st.button("DALLE") and text_input:
        img_response = openai.Image.create(prompt=text_input, n=3, size='256x256')
        image_urls = [img_response.data[idx].url for idx in range(len(img_response))]
        st.image(image_urls)
    else:
        st.image(DEFAULT_IMG_URL, width=500)

        
def get_semantic_search_results(question):
    whoami = "I am a highly intelligent question answering bot against lowering CO2 emission. If you comment about your plan for popular eco-friendly solutions, I will answer with the side effects of those."
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=whoami + "\n\nQuestion:" + question + "\n\nAnswer:",
      temperature=0,
      max_tokens=4000,
      top_p=1,
      frequency_penalty=0.1,
      presence_penalty=0
    )
    response_summary = openai.Completion.create(
      model="text-davinci-002",
      prompt="Summarize this with keywords:\n\n" + response.choices[0].text,
      temperature=0,
      max_tokens=50,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    whoami3 = "I'm a climate change campaigner to help to make actions that the public can follow easily. I also consider which scenario you are in. If you tell me the potential risks and the scenario, I will let you know which actions to take."
    risks = response_summary.choices[0].text
    scenario = question
    response_actions = openai.Completion.create(
      model="text-davinci-002",
      prompt=whoami3+" \n\nPotential risks:\n"+risks+"\n\nScenario:\n"+scenario+"\n\nAction:\n",
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    results = response_actions.choices[0].text.split(sep='\n')
    return results

     

if __name__ == "__main__":
    init()
    question = get_search_question()
    #results = ["batteries", "aluminium usage", "electricity demand", "..."]
    results = get_semantic_search_results(question)
    return_search_results(results)
    # TODO: search results to suggested action
    actions = ["you can look for the production processes which are using less ... for batteries",
    "those materials could be picked insted of aluminium usage: ...",
    "to decrease electricity demand, ...",]
    suggest_actions(actions)
    tldr()
    
