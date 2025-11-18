import joblib
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SpamClassifierService:
    """Service for spam email classification"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained spam classification model"""
        try:
            if os.path.exists(self.model_path):
                loaded_data = joblib.load(self.model_path)
                
                # Handle different saved formats
                if isinstance(loaded_data, dict):
                    self.model = loaded_data.get('model')
                    self.vectorizer = loaded_data.get('vectorizer')
                else:
                    self.model = loaded_data
                    # Try to load vectorizer separately
                    vectorizer_path = self.model_path.replace('.pkl', '_vectorizer.pkl')
                    if os.path.exists(vectorizer_path):
                        self.vectorizer = joblib.load(vectorizer_path)
                
                logger.info(f"Spam classifier model loaded from {self.model_path}")
            else:
                logger.warning(f"Model file not found: {self.model_path}")
                logger.info("Service will run in mock mode")
        except Exception as e:
            logger.error(f"Error loading spam model: {e}")
            logger.info("Service will run in mock mode")
    
    def classify(self, email_text: str) -> Dict[str, Any]:
        """
        Classify an email as spam or not spam
        
        Args:
            email_text: The email text to classify
            
        Returns:
            Dictionary with classification results
        """
        try:
            if self.model is None:
                # Mock response when model is not loaded
                return self._mock_classification(email_text)
            
            # Vectorize the text
            if self.vectorizer:
                features = self.vectorizer.transform([email_text])
            else:
                # If no vectorizer, use simple features (fallback)
                features = [[len(email_text), email_text.count(' ')]]
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Get probability if available
            confidence = None
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(features)[0]
                confidence = float(max(probabilities))
            else:
                confidence = 0.85  # Default confidence
            
            is_spam = bool(prediction == 1 or prediction == 'spam')
            
            return {
                "is_spam": is_spam,
                "prediction": "spam" if is_spam else "legitimate",
                "confidence": confidence,
                "details": self._get_details(email_text, is_spam, confidence)
            }
            
        except Exception as e:
            logger.error(f"Error in spam classification: {e}")
            return self._mock_classification(email_text)
    
    def _mock_classification(self, email_text: str) -> Dict[str, Any]:
        """Mock classification when model is not available"""
        # Simple heuristic for demo purposes
        spam_keywords = ['win', 'prize', 'click here', 'congratulations', 'free money', 
                         'urgent', 'act now', 'limited time', 'call now', '$$$']
        
        text_lower = email_text.lower()
        spam_count = sum(1 for keyword in spam_keywords if keyword in text_lower)
        
        is_spam = spam_count >= 2
        confidence = min(0.6 + (spam_count * 0.1), 0.95)
        
        return {
            "is_spam": is_spam,
            "prediction": "spam" if is_spam else "legitimate",
            "confidence": confidence,
            "details": {
                "risk_level": "high" if is_spam else "low",
                "detected_patterns": spam_keywords[:spam_count] if is_spam else [],
                "mode": "demo"
            }
        }
    
    def _get_details(self, email_text: str, is_spam: bool, confidence: float) -> Dict[str, Any]:
        """Get additional details about the classification"""
        risk_level = "high" if is_spam and confidence > 0.8 else \
                     "medium" if is_spam else "low"
        
        return {
            "risk_level": risk_level,
            "email_length": len(email_text),
            "detected_patterns": self._detect_patterns(email_text) if is_spam else []
        }
    
    def _detect_patterns(self, text: str) -> list[str]:
        """Detect common spam patterns"""
        patterns = []
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['click', 'link', 'http']):
            patterns.append("suspicious_links")
        if any(word in text_lower for word in ['urgent', 'act now', 'limited time']):
            patterns.append("urgency_language")
        if any(word in text_lower for word in ['win', 'prize', 'winner']):
            patterns.append("prize_claim")
        if any(word in text_lower for word in ['money', 'cash', '$']):
            patterns.append("money_references")
        
        return patterns
