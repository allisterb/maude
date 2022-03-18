import os, sys
import json
from logging import info, error, warn, debug

from googleapiclient import discovery

from text.spacy import nlp
from base.timer import begin
from core.text_classifier import TextClassifier

api_key = None

class TextClassifier(TextClassifier):
    def __init__(self, args=[]):
            super().__init__("Google Perspective Text Classifier", args)

    def print_model_info(self):
        pass

    def classify(self, text:str): 
        "Classify a span of text."""
        with begin("Classifying using Google Perspective API") as op:
            client = discovery.build(
                "commentanalyzer", "v1alpha1",
                developerKey=api_key,
                discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                static_discovery=False,
            )

            analyze_request = {
            'comment': { 'text': text },
            'requestedAttributes': {'TOXICITY': {}}
            }
            response = client.comments().analyze(body=analyze_request).execute()
            print(json.dumps(response, indent=2))
            op.complete()
   