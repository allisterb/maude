from logging import debug

from googleapiclient import discovery

from base.timer import begin
from core.text_classifier import TextClassifier

api_key = None

standard_attributes = {
    'TOXICITY': {}, 
    'SEVERE_TOXICITY': {}, 
    'IDENTITY_ATTACK':{}, 
    'INSULT':{},
    'THREAT':{}
}

experimental_attributes = {
    'TOXICITY_EXPERIMENTAL': {}, 
    'SEVERE_TOXICITY_EXPERIMENTAL': {}, 
    'IDENTITY_ATTACK_EXPERIMENTAL':{}, 
    'INSULT_EXPERIMENTAL':{},
    'THREAT_EXPERIMENTAL':{},
    'SEXUALLY_EXPLICIT': {},
    'FLIRTATION': {}
}

class TextClassifier(TextClassifier):
    def __init__(self, args=[]):
            super().__init__("Google Perspective Text Classifier", args)

    def print_model_info(self):
        pass

    def classify(self, text:str, use_experimental_attributes=False): 
        assert api_key != ''
        with begin("Classifying text span using Google Perspective API") as op:
            client = discovery.build(
                "commentanalyzer", "v1alpha1",
                developerKey=api_key,
                discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                static_discovery=False,
            )
            analyze_request = {
                'comment': { 'text': text },
                'requestedAttributes': standard_attributes if not use_experimental_attributes else experimental_attributes
            }
            response = client.comments().analyze(body=analyze_request).execute()
            debug(f'Received response: {response}')
            op.complete()
            return response
   