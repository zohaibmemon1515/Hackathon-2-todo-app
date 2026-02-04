"""
Language Detection Utility for AI Agent Enhancement
Detects and processes Roman Urdu input for the enhanced AI agent
"""

from typing import Tuple, Dict, Optional
import re
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Set seed for consistent results
DetectorFactory.seed = 0

class LanguageDetectionUtil:
    """
    Utility class for detecting and processing different languages,
    particularly Roman Urdu for the enhanced AI agent functionality.
    """

    # Common Roman Urdu patterns and phrases
    URDU_PATTERNS = {
        r'\b(check|dekh|dekho|dikhao|dikhaye)\s+(pending|kaam|kam|tasks|work)\b': 'check pending tasks',
        r'\b(kal|tomorrow|aaj|today)\s+(subah|sawere|morning)\s+(\d+)\s+(bajay|baje|at)\s+(pending|kaam|kam|tasks|work)\b': 'check pending tasks for tomorrow morning at time',
        r'\b(kal|tomorrow|aaj|today)\s+(\d+)\s+(bajay|baje|at)\s+(mujhe|me|to|for)\s+(yaad|yad|remind)\s+(dene|dena|do)\b': 'remind me tomorrow at time',
        r'\b(mujhe|me|to|for)\s+(yaad|yad|remind)\s+(dene|dena|do)\s+(kal|tomorrow|aaj|today)\s+(\d+)\s+(bajay|baje|at)\b': 'remind me tomorrow at time',
        r'\b(pending|kaam|kam|tasks|work)\s+(check|dekh|dekho|dikhao)\b': 'check pending tasks',
        r'\b(kal|tomorrow)\s+(subah|sawere|morning|raat|night|shaam|evening)\s+(\d+)\s+(bajay|baje|at)\s+(mujhe|me|to|for)\s+(yaad|yad|remind)\b': 'remind me tomorrow at time',
        r'\b(mujhe|me|to|for)\s+(kal|tomorrow)\s+(\d+)\s+(bajay|baje|at)\s+(yaad|yad|remind)\b': 'remind me tomorrow at time',
    }

    # Roman Urdu to English mappings for common phrases
    URDU_TO_ENGLISH_MAP = {
        'kal': 'tomorrow',
        'aaj': 'today',
        'subah': 'morning',
        'shaam': 'evening',
        'raat': 'night',
        'sawere': 'morning',
        'bajay': 'at',
        'baje': 'at',
        'mujhe': 'me',
        'yaad': 'remind',
        'yad': 'remind',
        'dene': 'give',
        'dena': 'give',
        'dijeye': 'give',
        'diya': 'given',
        'kaam': 'tasks',
        'kam': 'tasks',
        'dekh': 'check',
        'dekho': 'check',
        'dikhao': 'show',
        'dikhaye': 'show',
        'pending': 'pending',
        'tasks': 'tasks',
        'work': 'work',
        'check': 'check',
        'karne': 'to do',
        'karna': 'to do',
        'karo': 'do',
        'krna': 'do',
        'krne': 'to do'
    }

    @staticmethod
    def detect_language(text: str) -> Tuple[str, float]:
        """
        Detect the language of the given text.

        Args:
            text: Input text to analyze

        Returns:
            Tuple of (language_code, confidence_score)
        """
        if not text or not isinstance(text, str):
            return 'und', 0.0

        try:
            # Clean text for better detection
            clean_text = re.sub(r'[^\w\s]', ' ', text.lower()).strip()

            if len(clean_text.split()) == 0:
                return 'und', 0.0

            # Use langdetect to identify language
            detected_lang = detect(clean_text)

            # For basic confidence estimation
            # In a real implementation, you might want to use a more sophisticated approach
            confidence = 0.8 if detected_lang else 0.0

            return detected_lang, confidence
        except LangDetectException:
            # If detection fails, return 'und' for undefined
            return 'und', 0.0
        except Exception:
            return 'und', 0.0

    @staticmethod
    def is_urdu_or_roman_urdu(text: str) -> bool:
        """
        Check if the text contains Urdu or Roman Urdu content.

        Args:
            text: Input text to analyze

        Returns:
            Boolean indicating if text is likely Urdu or Roman Urdu
        """
        if not text:
            return False

        # Check for common Roman Urdu patterns
        text_lower = text.lower()

        # Look for common Roman Urdu words
        roman_urdu_indicators = [
            'kal', 'aaj', 'subah', 'shaam', 'raat', 'sawere', 'bajay', 'baje',
            'mujhe', 'yaad', 'yad', 'dene', 'dena', 'dijeye', 'diya',
            'kaam', 'kam', 'dekh', 'dekho', 'dikhao', 'dikhaye'
        ]

        for indicator in roman_urdu_indicators:
            if indicator in text_lower:
                return True

        # Check for Arabic/Persian script characters (indicating actual Urdu)
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        if arabic_pattern.search(text):
            return True

        # Try language detection
        lang, confidence = LanguageDetectionUtil.detect_language(text)
        return lang == 'ur' and confidence > 0.5

    @staticmethod
    def preprocess_urdu_command(text: str) -> Tuple[str, str, float]:
        """
        Preprocess Roman Urdu command by translating to English equivalent.

        Args:
            text: Original command text

        Returns:
            Tuple of (translated_text, detected_language, confidence)
        """
        if not text:
            return text, 'und', 0.0

        original_text = text
        processed_text = text.lower().strip()

        # First, try to detect language
        detected_lang, confidence = LanguageDetectionUtil.detect_language(processed_text)

        # If it's already English, return as is
        if detected_lang == 'en':
            return original_text, detected_lang, confidence

        # If it looks like Roman Urdu, translate common phrases
        if LanguageDetectionUtil.is_urdu_or_roman_urdu(original_text):
            # Apply mappings for common Roman Urdu phrases
            for urdu_word, english_word in LanguageDetectionUtil.URDU_TO_ENGLISH_MAP.items():
                processed_text = re.sub(rf'\b{re.escape(urdu_word)}\b', english_word, processed_text, flags=re.IGNORECASE)

            # Apply pattern-based translations
            for pattern, replacement in LanguageDetectionUtil.URDU_PATTERNS.items():
                if re.search(pattern, processed_text, re.IGNORECASE):
                    processed_text = replacement
                    break

            return processed_text, 'ur', max(confidence, 0.7)  # Boost confidence for Roman Urdu detection

        return original_text, detected_lang, confidence

    @staticmethod
    def translate_to_english_if_urdu(text: str) -> Dict[str, any]:
        """
        Translate Urdu/Roman Urdu text to English if needed.

        Args:
            text: Input text to potentially translate

        Returns:
            Dictionary with original_text, processed_text, language, confidence
        """
        if not text:
            return {
                'original_text': '',
                'processed_text': '',
                'language': 'und',
                'confidence': 0.0,
                'is_translated': False
            }

        # Detect language and preprocess
        processed_text, detected_lang, confidence = LanguageDetectionUtil.preprocess_urdu_command(text)

        is_translated = processed_text.lower() != text.lower()

        return {
            'original_text': text,
            'processed_text': processed_text,
            'language': detected_lang,
            'confidence': confidence,
            'is_translated': is_translated
        }


# Convenience function for external use
def detect_and_process_language(text: str) -> Dict[str, any]:
    """
    Main function to detect language and process accordingly.

    Args:
        text: Input text to analyze and process

    Returns:
        Dictionary with analysis results
    """
    return LanguageDetectionUtil.translate_to_english_if_urdu(text)