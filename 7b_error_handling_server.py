"""
Flask server for Emotion Detection API
Web deployment of the Emotion Detection application using Flask
Enhanced with comprehensive error handling for blank input errors
"""
from flask import Flask, request, jsonify
from EmotionDetection.emotion_detection import detect_emotion, validate_emotion_text


app = Flask(__name__)


@app.route('/emotion', methods=['POST'])
def emotion_detection():
    """
    Endpoint to detect emotions from the provided text
    
    Expected JSON:
    {
        "text": "your text here"
    }
    
    Returns on Success (200):
    {
        "status_code": 200,
        "text": "your text here",
        "emotions": {
            "anger": 0.123,
            "disgust": 0.045,
            "fear": 0.087,
            "joy": 0.698,
            "sadness": 0.047
        },
        "message": "Success"
    }
    
    Error Response on Blank Input (400 Bad Request):
    {
        "error": "Invalid input: Text cannot be empty",
        "status_code": 400,
        "message": "Bad Request - Text is empty"
    }
    
    Error Response on Missing JSON (400):
    {
        "error": "No JSON data provided",
        "status_code": 400,
        "message": "Bad Request - Missing JSON data"
    }
    
    Error Response on Missing Text Field (400):
    {
        "error": "Missing text field",
        "status_code": 400,
        "message": "Bad Request - Text field is required"
    }
    """
    
    # Error Handling Step 1: Check if JSON data was provided
    if not request.is_json:
        return jsonify({
            'error': 'Invalid content type. Expected application/json',
            'status_code': 400,
            'message': 'Bad Request - Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    # Error Handling Step 2: Check if data is empty
    if not data:
        return jsonify({
            'error': 'No JSON data provided',
            'status_code': 400,
            'message': 'Bad Request - Missing JSON data'
        }), 400
    
    # Error Handling Step 3: Check if 'text' field exists
    if 'text' not in data:
        return jsonify({
            'error': 'Missing text field',
            'status_code': 400,
            'message': 'Bad Request - Text field is required'
        }), 400
    
    text = data['text']
    
    # Error Handling Step 4: Validate text input (handles blank input)
    is_valid, error_response = validate_emotion_text(text)
    if not is_valid:
        return jsonify(error_response), error_response.get('status_code', 400)
    
    # Call emotion detection function
    result = detect_emotion(text)
    
    # Error Handling Step 5: Check result status code
    if 'status_code' in result:
        status_code = result['status_code']
        return jsonify(result), status_code
    
    # For backward compatibility
    if 'error' in result:
        return jsonify(result), 400
    
    # Success response
    return jsonify({
        'status_code': 200,
        'text': text,
        'emotions': result,
        'message': 'Success'
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    
    Returns:
    {
        "status": "healthy"
    }
    """
    return jsonify({'status': 'healthy'}), 200


@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with API documentation
    
    Returns API information and available endpoints
    """
    return jsonify({
        'message': 'Emotion Detection API',
        'version': '1.0.0',
        'endpoints': {
            'POST /emotion': 'Detect emotions from text',
            'GET /health': 'Health check',
            'GET /': 'API information'
        }
    })


@app.route('/error-examples', methods=['GET'])
def error_examples():
    """
    Returns example error responses for different error scenarios
    
    Demonstrates all possible error responses
    """
    return jsonify({
        'title': 'Error Handling Examples',
        'errors': [
            {
                'error_type': 'Blank Input Error',
                'status_code': 400,
                'example': {
                    'error': 'Invalid input: Text cannot be empty',
                    'status_code': 400,
                    'message': 'Bad Request - Text is empty'
                },
                'description': 'Returned when text field is empty or contains only whitespace'
            },
            {
                'error_type': 'Missing Text Field',
                'status_code': 400,
                'example': {
                    'error': 'Missing text field',
                    'status_code': 400,
                    'message': 'Bad Request - Text field is required'
                },
                'description': 'Returned when text field is not provided in JSON'
            },
            {
                'error_type': 'Missing JSON Data',
                'status_code': 400,
                'example': {
                    'error': 'No JSON data provided',
                    'status_code': 400,
                    'message': 'Bad Request - Missing JSON data'
                },
                'description': 'Returned when request body is empty'
            },
            {
                'error_type': 'Invalid Content Type',
                'status_code': 400,
                'example': {
                    'error': 'Invalid content type. Expected application/json',
                    'status_code': 400,
                    'message': 'Bad Request - Content-Type must be application/json'
                },
                'description': 'Returned when Content-Type is not application/json'
            },
            {
                'error_type': 'Invalid Input Type',
                'status_code': 400,
                'example': {
                    'error': 'Invalid input type: Expected string, got int',
                    'status_code': 400,
                    'message': 'Bad Request - Text must be a string'
                },
                'description': 'Returned when text is not a string'
            },
            {
                'error_type': 'Authentication Error',
                'status_code': 401,
                'example': {
                    'error': 'Authentication failed: Invalid API key',
                    'status_code': 401,
                    'message': 'Unauthorized - Invalid API credentials'
                },
                'description': 'Returned when Watson NLP API credentials are invalid'
            },
            {
                'error_type': 'Server Error',
                'status_code': 500,
                'example': {
                    'error': 'Unexpected error: Service error',
                    'status_code': 500,
                    'message': 'Internal Server Error - Unexpected exception occurred'
                },
                'description': 'Returned when an unexpected server error occurs'
            },
            {
                'error_type': 'Service Unavailable',
                'status_code': 503,
                'example': {
                    'error': 'Connection failed: Cannot connect to API',
                    'status_code': 503,
                    'message': 'Service Unavailable - Cannot reach API'
                },
                'description': 'Returned when Watson NLP API is unreachable'
            }
        ]
    })


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors"""
    return jsonify({
        'error': 'Bad Request',
        'status_code': 400,
        'message': str(error)
    }), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'status_code': 404,
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 Internal Server errors"""
    return jsonify({
        'error': 'Internal Server Error',
        'status_code': 500,
        'message': 'An unexpected server error occurred'
    }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
