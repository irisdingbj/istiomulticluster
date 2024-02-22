# File name: translator_gpu.py
# This file deploys a translator application on gpu machines.
# The translator application uses a pre-trained model from the transformers library.

from starlette.requests import Request

from ray import serve

from transformers import pipeline

# Creates a Ray Serve deployment for a translator application.
# Refer to https://docs.ray.io/en/latest/serve/scaling-and-resource-allocation.html# for more information.
@serve.deployment()
class Translator:
    def __init__(self):
        # Load model
        # Device map allows for automatic placement of the model on the available GPUs
        self.model = pipeline("translation_en_to_fr", model="t5-small", device_map="auto")

    def translate(self, text: str) -> str:
        # Run inference
        model_output = self.model(text)

        # Post-process output to return only the translation text
        translation = model_output[0]["translation_text"]

        return translation

    # Asynchronously calls the translate function.
    async def __call__(self, http_request: Request) -> str:
        english_text: str = await http_request.json()
        translation = self.translate(english_text)
        return translation

# Deploy the Translator class
translator_app = Translator.bind()