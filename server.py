"""
Flask server for Emotion Detection API
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
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
