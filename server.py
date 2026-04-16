"""
Flask server for Emotion Detection API
Web deployment of the Emotion Detection application using Flask
"""
from flask import Flask, request, jsonify
from EmotionDetection.emotion_detection import detect_emotion


app = Flask(__name__)


@app.route('/emotion', methods=['POST'])
def emotion_detection():
    """
    Endpoint to detect emotions from the provided text
    
    Expected JSON:
    {
        "text": "your text here"
    }
    
    Returns:
    {
        "status_code": 200,
        "emotions": {
            "anger": 0.123,
            "disgust": 0.045,
            "fear": 0.087,
            "joy": 0.698,
            "sadness": 0.047
        },
        "message": "Success"
    }
    
    Error Response (400 Bad Request):
    {
        "error": "Invalid input: Text cannot be empty",
        "status_code": 400,
        "message": "Bad Request - Text is empty"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'No JSON data provided',
            'status_code': 400,
            'message': 'Bad Request - Missing JSON data'
        }), 400
    
    if 'text' not in data:
        return jsonify({
            'error': 'Missing text field',
            'status_code': 400,
            'message': 'Bad Request - Text field is required'
        }), 400
    
    text = data['text']
    result = detect_emotion(text)
    
    # Check if result contains a status code
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
            'GET /': 'API documentation'
        }
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
