#%%
import openai
import json
import pathlib
import numpy as np
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv('OPENAI_API_KEY')
USER = os.getenv('USER')

if not API_KEY:
    raise ValueError("API_KEY environment variable is not set. Please check your .env file.")
if not USER:
    raise ValueError("USER environment variable is not set. Please check your .env file.")

openai.api_key = API_KEY
client = openai.OpenAI()
#%% Example Description Generation for FGVCAircraft
# from torchvision.datasets import FGVCAircraft

# AIRCRAFT_DIR = 'your_path/fgvcaircraft'
# data_dir = pathlib.Path(AIRCRAFT_DIR)
# dataset = FGVCAircraft(data_dir, split='test', annotation_level='family', download=True)
# classnames = dataset.classes

# WIKIART dataset
from datasets import load_dataset

WIKIART_DIR = f'/scratch-shared/{USER}/waffle-data/WIKIART'
data_dir = pathlib.Path(WIKIART_DIR)
dataset = load_dataset("huggan/wikiart", cache_dir=data_dir)
classnames = dataset['train'].features['genre'].names
print(classnames)

#%% Generate Prompts.
def generate_prompt(category_name: str):
    # you can replace the examples with whatever you want; these were random and worked, could be improved
    return f"""Q: What are useful visual features for distinguishing a lemur in a photo?
A: There are several useful visual features to tell there is a lemur in a photo:
- four-limbed primate
- black, grey, white, brown, or red-brown
- wet and hairless nose with curved nostrils
- long tail
- large eyes
- furry bodies
- clawed hands and feet
Q: What are useful visual features for distinguishing a television in a photo?
A: There are several useful visual features to tell there is a television in a photo:
- electronic device
- black or grey
- a large, rectangular screen
- a stand or mount to support the screen
- one or more speakers
- a power cord
- input ports for connecting to other devices
- a remote control
Q: What are useful features for distinguishing a {category_name} in a photo?
A: There are several useful visual features to tell there is a {category_name} in a photo:
-
"""

prompts = [generate_prompt(_c) for _c in classnames]
print(*prompts, sep='\n')

# #%% Query GPT-3.
# def stringtolist(description):
#     return [descriptor[2:] for descriptor in description.split('\n') if (descriptor != '') and (descriptor.startswith('- '))]

# descriptions = []
# reqs = 0
# for i, prompt in enumerate(prompts):
#     st = time.time()
#     response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {
#         "role": "user",
#         "content": prompt
#         }
#     ],
#     temperature=0.7,
#     max_tokens=100,
#     )
    
#     # response = openai.Completion.create(
#     #     model="text-embedding-3-large",
#     #     prompt=prompts[i:i + 20],
#     #     temperature=0.7,
#     #     max_tokens=100,
#     # )
#     print(i, ":", time.time() - st)
#     reqs += 1
#     descriptions += [stringtolist(_r["text"]) for _r in response["choices"]]
#     # deal with rate limit
#     if reqs > 2:
#         time.sleep(61)
#         reqs = 0

# #%% Write generated descriptions to JSON.
# descriptions_dict = {_c: _d for _c, _d in zip(dataset.classes, descriptions)}
# with open('descriptors/descriptors_wikiart.json', 'w') as outfile:
#     outfile.write(json.dumps(descriptions_dict, indent=4))
