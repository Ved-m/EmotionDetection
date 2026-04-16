"""
Emotion Detection Module using IBM Watson NLP
Enhanced with error handling and HTTP status codes
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
              
    Raises:
        ValueError: If text input is invalid (None or not a string)
        Exception: If Watson API fails
    """
    # Input validation for status code 400
    if text is None:
        return {
            'error': 'Invalid input: Text cannot be None',
            'status_code': 400,
            'message': 'Bad Request - Missing text parameter'
        }
    
    if not isinstance(text, str):
        return {
            'error': f'Invalid input type: Expected string, got {type(text).__name__}',
            'status_code': 400,
            'message': 'Bad Request - Text must be a string'
        }
    
    if len(text.strip()) == 0:
        return {
            'error': 'Invalid input: Text cannot be empty',
            'status_code': 400,
            'message': 'Bad Request - Text is empty'
        }
    
    # Initialize Watson NLU
    try:
        authenticator = IAMAuthenticator(apikey='YOUR_API_KEY')
        nlu = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=authenticator,
            service_url='YOUR_SERVICE_URL'
        )
    except Exception as auth_error:
        return {
            'error': f'Authentication failed: {str(auth_error)}',
            'status_code': 401,
            'message': 'Unauthorized - Invalid API credentials'
        }
    
    try:
        # Analyze text with Watson NLU
        response = nlu.analyze(
            text=text,
            features={
                'emotion': {}
            }
        )
        
        # Extract emotions from response
        emotions = response.result['emotion']['document']['emotion']
        
        # Format emotions with proper structure
        formatted_emotions = {}
        for emotion, score in emotions.items():
            # Round scores to 3 decimal places
            formatted_emotions[emotion] = round(score, 3)
        
        return {
            'status_code': 200,
            'emotions': formatted_emotions,
            'message': 'Success'
        }
    
    except ValueError as value_error:
        # Handle value-related errors (400 Bad Request)
        return {
            'error': f'Bad Request: {str(value_error)}',
            'status_code': 400,
            'message': 'Bad Request - Invalid request format'
        }
    
    except KeyError as key_error:
        # Handle missing keys in response
        return {
            'error': f'Response parsing error: {str(key_error)}',
            'status_code': 500,
            'message': 'Internal Server Error - Response format issue'
        }
    
    except ConnectionError as conn_error:
        # Handle connection errors
        return {
            'error': f'Connection failed: {str(conn_error)}',
            'status_code': 503,
            'message': 'Service Unavailable - Cannot reach API'
        }
    
    except Exception as e:
        # Handle all other exceptions (500 Internal Server Error)
        return {
            'error': f'Unexpected error: {str(e)}',
            'status_code': 500,
            'message': 'Internal Server Error - Unexpected exception occurred'
        }


def validate_emotion_text(text):
    """
    Validate text input for emotion detection
    
    Args:
        text: The text to validate
    
    Returns:
        tuple: (is_valid: bool, error_response: dict or None)
    """
    # Check if text is None
    if text is None:
        return False, {
            'error': 'Invalid input: Text cannot be None',
            'status_code': 400
        }
    
    # Check if text is a string
    if not isinstance(text, str):
        return False, {
            'error': f'Invalid input type: Expected string, got {type(text).__name__}',
            'status_code': 400
        }
    
    # Check if text is empty
    if len(text.strip()) == 0:
        return False, {
            'error': 'Invalid input: Text cannot be empty',
            'status_code': 400
        }
    
    # Check text length (optional validation)
    if len(text) > 10000:
        return False, {
            'error': 'Text too long: Maximum 10000 characters allowed',
            'status_code': 413
        }
    
    return True, None
