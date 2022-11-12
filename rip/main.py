import openai
from api_secrets import API_KEY

openai.api_key = API_KEY
prompt = """A neutron star is the collapsed core of a massive supergiant star, 
which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] 
Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, 
and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] 
They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\n

Tl;dr"""

text_response = openai.Completion.create(
  model="text-davinci-002",
  prompt=prompt,
  temperature=0.7,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
tldr_text = text_response.choices[0].text

img_response = openai.Image.create(
  prompt=tldr_text,
  n=1,
  size="1024x1024"
)
image_url = img_response.data[0].url

print(image_url)