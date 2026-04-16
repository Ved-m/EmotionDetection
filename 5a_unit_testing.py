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
    
    def test_detect_emotion_returns_dictionary(self):
        """Test that detect_emotion always returns a dictionary"""
        texts = [
            "I love this!",
            "This is terrible",
            "I'm feeling neutral",
            ""
        ]
        for text in texts:
            result = detect_emotion(text)
            self.assertTrue(isinstance(result, dict), 
                          f"Expected dict for text: {text}")
    
    def test_detect_emotion_score_range(self):
        """Test that emotion scores are in valid range (0-1)"""
        text = "I am happy and sad at the same time"
        result = detect_emotion(text)
        
        if 'error' not in result:
            for emotion, score in result.items():
                self.assertGreaterEqual(score, 0.0, 
                                       f"Score for {emotion} is below 0")
                self.assertLessEqual(score, 1.0, 
                                    f"Score for {emotion} is above 1")
    
    def test_detect_emotion_error_handling(self):
        """Test error handling for invalid inputs"""
        result = detect_emotion(None)
        # Result should be either a dict of emotions or an error dict
        self.assertIsInstance(result, dict)
    
    def test_detect_emotion_with_special_characters(self):
        """Test emotion detection with special characters"""
        text = "I'm @#$% excited about this!!! 🎉"
        result = detect_emotion(text)
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
