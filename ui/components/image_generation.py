import openai
import streamlit as st

def generate_image(text_input):
    img_response = openai.Image.create(prompt=f"{text_input} a cartoon image", n=3, size="256x256")
    image_urls = [img_response.data[idx].url for idx in range(len(img_response))]
    st.image(image_urls)