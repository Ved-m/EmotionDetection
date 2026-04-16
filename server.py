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
        "text": "your text here",
        "emotions": {
            "anger": 0.123,
            "disgust": 0.045,
            "fear": 0.087,
            "joy": 0.698,
            "sadness": 0.047
        }
    }
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    emotions = detect_emotion(text)
    
    return jsonify({
        'text': text,
        'emotions': emotions
    })


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
