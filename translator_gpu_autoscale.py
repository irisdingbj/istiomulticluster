# File name: translator_autoscale.py
# This file deploys a translator application on gpu machines with autoscaling.
# The translator application uses a pre-trained model from the transformers library.

from starlette.requests import Request

from ray import serve

from transformers import pipeline

# Creates a Ray Serve deployment for a translator application.
# Refer to https://docs.ray.io/en/latest/serve/scaling-and-resource-allocation.html# for more information.
@serve.deployment(
    autoscaling_config={
        "min_replicas": 2,
        "initial_replicas": 2,
        "max_replicas": 8,
        "upscale_delay_s": 2,
        "downscale_delay_s": 60,
    }
)
class Translator:
    def __init__(self):
        # Load model
        # Device map allows for automatic placement of the model on the available GPUs
        self.model = pipeline("translation_en_to_fr", model="t5-small", device_map="auto")
        # self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small", low_cpu_mem_usage=True)

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