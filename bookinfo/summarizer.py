# File name: summarizer.py
# This file deploys a summarizer app that summarizes and translates text.
# The Translator and Summarizer classes are defined as Ray Serve deployments.
# Both deployments use a pipeline of model T5-small from the transformers library.

from starlette.requests import Request

from ray import serve
from ray.serve.handle import RayServeHandle

from transformers import pipeline

# Creates a Ray Serve deployment for the translator
@serve.deployment
class Translator:
    def __init__(self):
        # Load model
        self.model = pipeline("translation_en_to_fr", model="t5-small")

    def translate(self, text: str) -> str:
        # Run inference
        model_output = self.model(text)

        # Post-process output to return only the translation text
        translation = model_output[0]["translation_text"]

        return translation

# Creates a Ray Serve deployment for the summarizer
@serve.deployment
class Summarizer:
    def __init__(self, translator: RayServeHandle):
        # Load model
        self.model = pipeline("summarization", model="t5-small")
        self.translator = translator

    def summarize(self, text: str) -> str:
        # Run inference
        model_output = self.model(text, min_length=5, max_length=15)

        # Post-process output to return only the summary text
        summary = model_output[0]["summary_text"]

        return summary

    async def __call__(self, http_request: Request) -> str:
        english_text: str = await http_request.json()
        summary = self.summarize(english_text)

        translation_ref = await self.translator.translate.remote(summary)
        translation = await translation_ref

        return translation

# Binds the translator and summarizer deployments to the same deployment.
summarizer = Summarizer.bind(Translator.bind())