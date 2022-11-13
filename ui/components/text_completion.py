import openai
import streamlit as st
from typing import Dict, Any


""" for all possible parameters, see https://beta.openai.com/docs/api-reference/completions/create
Note that `best_of` >= `n` is required 
"""
_default_completion_parameters = {
    "temperature":0.7,
    "max_tokens":60,
    "top_p":1.0,
    "frequency_penalty":0.0,
    "presence_penalty":0.0,
    "n": 1,
    "best_of": 3,
    "stop":"\n",
    }

def get_default_completion_params() -> Dict[str, Any]:
    return _default_completion_parameters

def set_completion_params(param_dict: Dict[str, Any]) -> Dict[str, Any]:
    params = get_default_completion_params()
    return {k:  param_dict[k] if k in param_dict.keys() else v for k,v in params.items()}

@st.cache(suppress_st_warning=True, persist=True)
def transform_text_to_easy_text(text_input: str, **kwags) -> str:
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Summarize this for a second-grade student:\n\n{text_input}",
        **kwags,
    )
    return response.choices[0].text

@st.cache(suppress_st_warning=True, persist=True)
def transform_text_to_scene_description(text_input: str, **kwags) -> str:
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Here is a concept:\n\n{text_input} \n\nDescribe an image that represents this scene:",
        **kwags,
    )
    return response.choices[0].text

def get_semantic_search_results(question: str):
    whoami = "I am a highly intelligent question answering bot against lowering CO2 emission. If you comment about your plan for popular eco-friendly solutions, I will answer with the side effects of those."
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=whoami + "\n\nQ: "+ question +"\nA:",
      temperature=0,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      best_of=3,
      stop=["\n"]
    )
    results = response.choices[0].text.split(sep='.')
    return results