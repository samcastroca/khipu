import joblib
import os
from typing import Dict, Any
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class PhishingURLService:
    """Service for phishing URL detection"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained phishing URL detection model"""
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
                
                logger.info(f"Phishing URL model loaded from {self.model_path}")
            else:
                logger.warning(f"Model file not found: {self.model_path}")
                logger.info("Service will run in mock mode")
        except Exception as e:
            logger.error(f"Error loading phishing URL model: {e}")
            logger.info("Service will run in mock mode")
    
    def check_url(self, url: str) -> Dict[str, Any]:
        """
        Check if a URL is a phishing attempt
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dictionary with detection results
        """
        try:
            if self.model is None:
                return self._mock_detection(url)
            
            # Extract features from URL
            features = self._extract_url_features(url)
            
            # Make prediction
            if self.vectorizer:
                feature_vector = self.vectorizer.transform([url])
            else:
                feature_vector = [features]
            
            prediction = self.model.predict(feature_vector)[0]
            
            # Get probability if available
            confidence = None
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(feature_vector)[0]
                confidence = float(max(probabilities))
            else:
                confidence = 0.82
            
            is_phishing = bool(prediction == 1 or prediction == 'phishing')
            
            return {
                "is_phishing": is_phishing,
                "prediction": "phishing" if is_phishing else "legitimate",
                "confidence": confidence,
                "details": self._get_details(url, is_phishing, confidence, features)
            }
            
        except Exception as e:
            logger.error(f"Error in phishing URL detection: {e}")
            return self._mock_detection(url)
    
    def _extract_url_features(self, url: str) -> list:
        """Extract features from URL for classification"""
        parsed = urlparse(url)
        
        features = [
            len(url),
            url.count('.'),
            url.count('-'),
            url.count('@'),
            url.count('?'),
            url.count('='),
            1 if parsed.scheme == 'https' else 0,
            len(parsed.netloc),
            1 if any(char.isdigit() for char in parsed.netloc) else 0,
        ]
        
        return features
    
    def _mock_detection(self, url: str) -> Dict[str, Any]:
        """Mock detection when model is not available"""
        parsed = urlparse(url)
        
        # Simple heuristics for demo
        suspicious_indicators = []
        score = 0
        
        # Check for suspicious patterns
        if parsed.scheme != 'https':
            suspicious_indicators.append('no_ssl')
            score += 2
        
        if any(char.isdigit() for char in parsed.netloc):
            suspicious_indicators.append('ip_address')
            score += 3
        
        if url.count('-') > 3:
            suspicious_indicators.append('excessive_hyphens')
            score += 1
        
        if url.count('.') > 4:
            suspicious_indicators.append('subdomain_abuse')
            score += 2
        
        suspicious_keywords = ['login', 'verify', 'account', 'secure', 'update', 
                              'bank', 'paypal', 'amazon']
        if any(keyword in url.lower() for keyword in suspicious_keywords):
            suspicious_indicators.append('suspicious_keywords')
            score += 2
        
        is_phishing = score >= 4
        confidence = min(0.5 + (score * 0.1), 0.92)
        
        return {
            "is_phishing": is_phishing,
            "prediction": "phishing" if is_phishing else "legitimate",
            "confidence": confidence,
            "details": {
                "risk_level": "high" if is_phishing else "low",
                "suspicious_features": suspicious_indicators,
                "mode": "demo"
            }
        }
    
    def _get_details(self, url: str, is_phishing: bool, confidence: float, 
                     features: list) -> Dict[str, Any]:
        """Get additional details about the detection"""
        parsed = urlparse(url)
        
        risk_level = "high" if is_phishing and confidence > 0.8 else \
                     "medium" if is_phishing else "low"
        
        suspicious_features = []
        if parsed.scheme != 'https':
            suspicious_features.append('no_ssl')
        if any(char.isdigit() for char in parsed.netloc):
            suspicious_features.append('ip_address')
        if url.count('.') > 4:
            suspicious_features.append('subdomain_abuse')
        
        return {
            "risk_level": risk_level,
            "url_length": len(url),
            "domain": parsed.netloc,
            "scheme": parsed.scheme,
            "suspicious_features": suspicious_features if is_phishing else []
        }
