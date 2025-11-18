import joblib
import os
from typing import Dict, Any
import logging
from urllib.parse import urlparse
from pathlib import Path

# Import tokenizer from separate module to ensure it's available for joblib
from app.services.url_tokenizer import tokenize_url

logger = logging.getLogger(__name__)


class PhishingURLService:
    """Service for phishing URL detection using TF-IDF and Logistic Regression"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained phishing URL detection model and TF-IDF vectorizer"""
        try:
            # Make tokenize_url available in __main__ namespace for joblib
            # This is needed when the vectorizer was pickled with a custom tokenizer
            import sys
            import __main__
            __main__.tokenize_url = tokenize_url
            
            # Determine vectorizer path
            # Expecting: phishing_url_logistic_regression.pkl and url_tfidf_vectorizer.pkl
            model_dir = Path(self.model_path).parent
            
            # Try to find vectorizer with common naming patterns
            vectorizer_candidates = [
                model_dir / "url_tfidf_vectorizer.pkl",
                model_dir / "phishing_url_classifier_vectorizer.pkl",
                str(self.model_path).replace('.pkl', '_vectorizer.pkl')
            ]
            
            vectorizer_path = None
            for candidate in vectorizer_candidates:
                if os.path.exists(candidate):
                    vectorizer_path = candidate
                    break
            
            # Load model
            if os.path.exists(self.model_path):
                loaded_data = joblib.load(self.model_path)
                
                # Handle different saved formats
                if isinstance(loaded_data, dict):
                    self.model = loaded_data.get('model')
                    self.vectorizer = loaded_data.get('vectorizer')
                else:
                    self.model = loaded_data
                
                logger.info(f"✅ Phishing URL model loaded from {self.model_path}")
            else:
                logger.warning(f"⚠️  Model file not found: {self.model_path}")
            
            # Load vectorizer separately if not already loaded
            if self.vectorizer is None and vectorizer_path:
                self.vectorizer = joblib.load(vectorizer_path)
                logger.info(f"✅ URL TF-IDF vectorizer loaded from {vectorizer_path}")
            elif self.vectorizer is None:
                logger.warning(f"⚠️  Vectorizer not found in any of: {vectorizer_candidates}")
                
            if self.model is None or self.vectorizer is None:
                logger.info("Service will run in mock mode")
                
        except Exception as e:
            logger.error(f"❌ Error loading phishing URL model: {e}")
            logger.info("Service will run in mock mode")
    
    def check_url(self, url: str) -> Dict[str, Any]:
        """
        Check if a URL is a phishing attempt using TF-IDF vectorization
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dictionary with detection results
        """
        try:
            if self.model is None or self.vectorizer is None:
                return self._mock_detection(url)
            
            # Vectorize URL using TF-IDF
            # The vectorizer uses a custom tokenizer that splits URLs by /, ., ?, =, &, -, _, :
            url_vector = self.vectorizer.transform([url])
            
            # Make prediction (0 = legitimate, 1 = phishing)
            prediction = self.model.predict(url_vector)[0]
            
            # Get probability
            confidence = None
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(url_vector)[0]
                # Use the probability of the predicted class
                if prediction == 0:
                    # Legitimate - use probability of class 0
                    confidence = float(probabilities[0])
                else:
                    # Phishing - use probability of class 1
                    confidence = float(probabilities[1])
            else:
                confidence = 0.82
            
            is_phishing = bool(prediction == 1)
            
            # Get risk factors based on URL patterns
            risk_factors = self._identify_risk_factors(url)
            
            return {
                "is_phishing": is_phishing,
                "prediction": "phishing" if is_phishing else "legitimate",
                "confidence": confidence,
                "details": {
                    "risk_level": "high" if is_phishing and confidence > 0.8 else 
                                  "medium" if is_phishing else "low",
                    "url_length": len(url),
                    "domain": urlparse(url).netloc,
                    "scheme": urlparse(url).scheme,
                    "risk_factors": risk_factors
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error in phishing URL detection: {e}")
            return self._mock_detection(url)
    
    def _identify_risk_factors(self, url: str) -> list:
        """
        Identify risk factors in the URL based on common phishing patterns
        
        Args:
            url: The URL to analyze
            
        Returns:
            List of identified risk factors
        """
        risk_factors = []
        parsed = urlparse(url)
        url_lower = url.lower()
        
        # Check for lack of SSL
        if parsed.scheme != 'https':
            risk_factors.append('no_ssl')
        
        # Check for IP address in domain
        if any(char.isdigit() for char in parsed.netloc) and '.' in parsed.netloc:
            # Simple check if domain looks like an IP
            parts = parsed.netloc.split('.')
            if len(parts) == 4 and all(p.isdigit() for p in parts):
                risk_factors.append('ip_address')
        
        # Check for excessive hyphens
        if url.count('-') > 3:
            risk_factors.append('excessive_hyphens')
        
        # Check for excessive subdomains
        if url.count('.') > 4:
            risk_factors.append('subdomain_abuse')
        
        # Check for suspicious keywords
        suspicious_keywords = ['login', 'verify', 'account', 'secure', 'update', 
                              'bank', 'paypal', 'amazon', 'confirm', 'suspended',
                              'password', 'billing', 'support']
        for keyword in suspicious_keywords:
            if keyword in url_lower:
                risk_factors.append(f'suspicious_keyword_{keyword}')
                break  # Only add one keyword warning
        
        # Check for unusual TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.zip', '.review']
        if any(url_lower.endswith(tld) for tld in suspicious_tlds):
            risk_factors.append('suspicious_tld')
        
        # Check for very long URLs
        if len(url) > 100:
            risk_factors.append('excessive_length')
        
        # Check for URL shorteners
        shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly']
        if any(shortener in url_lower for shortener in shorteners):
            risk_factors.append('url_shortener')
        
        return risk_factors
    
    def _mock_detection(self, url: str) -> Dict[str, Any]:
        """Mock detection when model is not available"""
        risk_factors = self._identify_risk_factors(url)
        
        # Calculate score based on risk factors
        score = len(risk_factors)
        
        is_phishing = score >= 3
        confidence = min(0.5 + (score * 0.1), 0.92)
        
        return {
            "is_phishing": is_phishing,
            "prediction": "phishing" if is_phishing else "legitimate",
            "confidence": confidence,
            "details": {
                "risk_level": "high" if is_phishing else "low",
                "url_length": len(url),
                "domain": urlparse(url).netloc,
                "scheme": urlparse(url).scheme,
                "risk_factors": risk_factors,
                "mode": "demo"
            }
        }
