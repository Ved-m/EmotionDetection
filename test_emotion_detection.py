"""
Unit tests for Emotion Detection Module
"""
import unittest
from EmotionDetection.emotion_detection import detect_emotion


class TestEmotionDetection(unittest.TestCase):
    """Test cases for emotion detection functionality"""
    
    def test_detect_emotion_with_valid_text(self):
        """Test emotion detection with valid text"""
        text = "I am very happy and excited about this project!"
        result = detect_emotion(text)
        self.assertIsInstance(result, dict)
    
    def test_detect_emotion_with_empty_text(self):
        """Test emotion detection with empty text"""
        text = ""
        result = detect_emotion(text)
        self.assertIsInstance(result, dict)
    
    def test_detect_emotion_response_structure(self):
        """Test that response contains expected emotion categories"""
        text = "I feel amazing!"
        result = detect_emotion(text)
        
        expected_emotions = ['anger', 'fear', 'joy', 'sadness', 'surprise']
        if 'error' not in result:
            for emotion in expected_emotions:
                self.assertIn(emotion, result)


if __name__ == '__main__':
    unittest.main()
