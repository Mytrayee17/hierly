import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDxYIfsEDSDvqVOLl5Y00bOEPQ9zE73vjE")

for m in genai.list_models():
    print(m.name)


