"""
Emotion Detection Module using IBM Watson NLP
"""
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def detect_emotion(text):
    """
    Detect emotions from the given text using IBM Watson NLU
    
    Args:
        text (str): The text to analyze for emotions
    
    Returns:
        dict: A dictionary containing emotion scores formatted to 3 decimal places
              Keys: anger, disgust, fear, joy, sadness
    """
    # Initialize Watson NLU
    authenticator = IAMAuthenticator(apikey='YOUR_API_KEY')
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
        
        # Format emotions with proper structure
        formatted_emotions = {}
        for emotion, score in emotions.items():
            # Round scores to 3 decimal places
            formatted_emotions[emotion] = round(score, 3)
        
        return formatted_emotions
    except Exception as e:
        return {'error': str(e)}
