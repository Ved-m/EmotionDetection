"""Emotion Detection Package

This package provides emotion detection functionality using IBM Watson NLP.
It analyzes text and returns emotion scores for anger, disgust, fear, joy, and sadness.

Example usage:
    from EmotionDetection.emotion_detection import detect_emotion
    
    result = detect_emotion("I am very happy!")
    print(result)
"""

from EmotionDetection.emotion_detection import detect_emotion

__version__ = "1.0.0"
__author__ = "Emotion Detection Team"
__all__ = ["detect_emotion"]

