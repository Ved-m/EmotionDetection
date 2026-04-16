# Emotion Detection App

This project uses IBM Watson NLP to detect emotions from text.
Built using Python and Flask.

## Project Structure

```
EmotionDetection/
│
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
│
├── test_emotion_detection.py
├── server.py
└── README.md
```

## Features

- Emotion detection using IBM Watson Natural Language Understanding API
- Flask REST API for easy integration
- Supports detection of multiple emotions: anger, fear, joy, sadness, surprise
- Unit tests included

## Prerequisites

- Python 3.7+
- IBM Watson NLP API credentials

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install flask ibm-watson
```

## Configuration

Before running the application, update the following in `EmotionDetection/emotion_detection.py`:
- `YOUR_API_KEY`: Your IBM Watson API key
- `YOUR_SERVICE_URL`: Your IBM Watson service URL

## Usage

### Starting the Server

```bash
python server.py
```

The server will run on `http://localhost:5000`

### API Endpoint

**POST** `/emotion`

Request body:
```json
{
    "text": "Your text here"
}
```

Response:
```json
{
    "text": "Your text here",
    "emotions": {
        "anger": 0.0,
        "fear": 0.0,
        "joy": 0.9,
        "sadness": 0.0,
        "surprise": 0.1
    }
}
```

## Testing

Run the unit tests:
```bash
python -m unittest test_emotion_detection.py
```

## License

MIT License
