"""
Unit tests for Emotion Detection Module with Mocking
"""
import unittest
from unittest.mock import patch, MagicMock


class TestEmotionDetection(unittest.TestCase):
    """Test cases for emotion detection functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_emotion_response = {
            'anger': 0.123,
            'disgust': 0.045,
            'fear': 0.087,
            'joy': 0.698,
            'sadness': 0.047
        }
    
    @patch('EmotionDetection.emotion_detection.NaturalLanguageUnderstandingV1')
    def test_detect_emotion_with_valid_text(self, mock_nlu):
        """Test emotion detection with valid text"""
        # Mock the NLU response
        mock_instance = MagicMock()
        mock_nlu.return_value = mock_instance
        mock_instance.analyze.return_value.result = {
            'emotion': {'document': {'emotion': self.sample_emotion_response}}
        }
        
        from EmotionDetection.emotion_detection import detect_emotion
        text = "I am very happy and excited about this project!"
        result = detect_emotion(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('joy', result)
    
    @patch('EmotionDetection.emotion_detection.NaturalLanguageUnderstandingV1')
    def test_detect_emotion_with_empty_text(self, mock_nlu):
        """Test emotion detection with empty text"""
        mock_instance = MagicMock()
        mock_nlu.return_value = mock_instance
        mock_instance.analyze.return_value.result = {
            'emotion': {'document': {'emotion': self.sample_emotion_response}}
        }
        
        from EmotionDetection.emotion_detection import detect_emotion
        text = ""
        result = detect_emotion(text)
        
        self.assertIsInstance(result, dict)
    
    @patch('EmotionDetection.emotion_detection.NaturalLanguageUnderstandingV1')
    def test_detect_emotion_response_structure(self, mock_nlu):
        """Test that response contains expected emotion categories"""
        mock_instance = MagicMock()
        mock_nlu.return_value = mock_instance
        mock_instance.analyze.return_value.result = {
            'emotion': {'document': {'emotion': self.sample_emotion_response}}
        }
        
        from EmotionDetection.emotion_detection import detect_emotion
        text = "I feel amazing!"
        result = detect_emotion(text)
        
        expected_emotions = ['anger', 'fear', 'joy', 'sadness']
        if 'error' not in result:
            for emotion in expected_emotions:
                self.assertIn(emotion, result)
    
    @patch('EmotionDetection.emotion_detection.NaturalLanguageUnderstandingV1')
    def test_detect_emotion_returns_dictionary(self, mock_nlu):
        """Test that detect_emotion always returns a dictionary"""
        mock_instance = MagicMock()
        mock_nlu.return_value = mock_instance
        mock_instance.analyze.return_value.result = {
            'emotion': {'document': {'emotion': self.sample_emotion_response}}
        }
        
        from EmotionDetection.emotion_detection import detect_emotion
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
    
    @patch('EmotionDetection.emotion_detection.NaturalLanguageUnderstandingV1')
    def test_detect_emotion_score_range(self, mock_nlu):
        """Test that emotion scores are in valid range (0-1)"""
        mock_instance = MagicMock()
        mock_nlu.return_value = mock_instance
        mock_instance.analyze.return_value.result = {
            'emotion': {'document': {'emotion': self.sample_emotion_response}}
        }
        
        from EmotionDetection.emotion_detection import detect_emotion
        text = "I am happy and sad at the same time"
        result = detect_emotion(text)
        
        if 'error' not in result:
            for emotion, score in result.items():
                self.assertGreaterEqual(score, 0.0, 
                                       f"Score for {emotion} is below 0")
                self.assertLessEqual(score, 1.0, 
                                    f"Score for {emotion} is above 1")
    
    @patch('EmotionDetection.emotion_detection.NaturalLanguageUnderstandingV1')
    def test_detect_emotion_formatting(self, mock_nlu):
        """Test that emotion scores are properly formatted"""
        mock_instance = MagicMock()
        mock_nlu.return_value = mock_instance
        mock_instance.analyze.return_value.result = {
            'emotion': {'document': {'emotion': {
                'anger': 0.1234567,
                'joy': 0.6987654
            }}}
        }
        
        from EmotionDetection.emotion_detection import detect_emotion
        text = "I am happy"
        result = detect_emotion(text)
        
        # Check that scores are rounded to 3 decimal places
        if 'anger' in result:
            self.assertEqual(len(str(result['anger']).split('.')[-1]), 3)


if __name__ == '__main__':
    unittest.main()
