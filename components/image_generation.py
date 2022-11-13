import openai
import streamlit as st

def generate_image(text_input):
    img_types = ["a cartoon image", "a realistic image", "a futuristic image"]
    image_urls = []
    for im_type in img_types:
        img_response = openai.Image.create(prompt=f"{text_input} {im_type}", n=1, size="256x256")
        image_urls.append(img_response.data[0].url)
    st.image(image_urls)