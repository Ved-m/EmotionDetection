"""
Emotion Detection Module using IBM Watson NLP
"""
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.authenticators import IAMAuthenticator


def detect_emotion(text):
    """
    Detect emotions from the given text using IBM Watson NLU
    
    Args:
        text (str): The text to analyze for emotions
    
    Returns:
        dict: A dictionary containing emotion scores for anger, fear, joy, sadness, and surprise
    """
    # Initialize Watson NLU
    authenticator = IAMAuthenticator({'apikey': 'YOUR_API_KEY'})
    nlu = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator,
        service_url='YOUR_SERVICE_URL'
    )
    
    try:
        response = nlu.analyze(
            text=text,
            features={
                'emotion': {}
            }
        )
        
        emotions = response.result['emotion']['document']['emotion']
        return emotions
    except Exception as e:
        return {'error': str(e)}
