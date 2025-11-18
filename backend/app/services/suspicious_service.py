import joblib
import os
from typing import Dict, Any
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class SuspiciousAccessService:
    """Service for suspicious access detection using ML pipeline"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained suspicious access detection pipeline"""
        try:
            if os.path.exists(self.model_path):
                self.pipeline = joblib.load(self.model_path)
                logger.info(f"✅ Suspicious access pipeline loaded from {self.model_path}")
            else:
                logger.warning(f"⚠️  Model file not found: {self.model_path}")
                logger.info("Service will run in mock mode")
        except Exception as e:
            logger.error(f"❌ Error loading suspicious access model: {e}")
            logger.info("Service will run in mock mode")
    
    def check_access(self, 
                     network_packet_size: int,
                     protocol_type: str,
                     login_attempts: int,
                     session_duration: float,
                     encryption_used: str,
                     ip_reputation_score: float,
                     failed_logins: int,
                     browser_type: str,
                     unusual_time_access: int) -> Dict[str, Any]:
        """
        Check if network access is suspicious/attack
        
        Args:
            network_packet_size: Size of network packet
            protocol_type: Protocol used (HTTP, HTTPS, FTP, SSH, etc.)
            login_attempts: Number of login attempts
            session_duration: Duration of session in minutes
            encryption_used: Encryption type (AES, RSA, None, Unknown)
            ip_reputation_score: IP reputation score (0-100)
            failed_logins: Number of failed logins
            browser_type: Browser type (Chrome, Firefox, Safari, Edge, etc.)
            unusual_time_access: Binary flag for unusual access time (0 or 1)
            
        Returns:
            Dictionary with detection results
        """
        try:
            if self.pipeline is None:
                return self._mock_detection(
                    network_packet_size, protocol_type, login_attempts,
                    session_duration, encryption_used, ip_reputation_score,
                    failed_logins, browser_type, unusual_time_access
                )
            
            # Create DataFrame with exact column names as in training
            data = pd.DataFrame([{
                "network_packet_size": network_packet_size,
                "protocol_type": protocol_type,
                "login_attempts": login_attempts,
                "session_duration": session_duration,
                "encryption_used": encryption_used,
                "ip_reputation_score": ip_reputation_score,
                "failed_logins": failed_logins,
                "browser_type": browser_type,
                "unusual_time_access": unusual_time_access
            }])
            
            # Make prediction (0 = normal, 1 = attack)
            prediction = self.pipeline.predict(data)[0]
            
            # Get probability
            confidence = None
            if hasattr(self.pipeline, 'predict_proba'):
                probabilities = self.pipeline.predict_proba(data)[0]
                # Use probability of predicted class
                if prediction == 0:
                    confidence = float(probabilities[0])
                else:
                    confidence = float(probabilities[1])
            else:
                confidence = 0.75
            
            is_attack = bool(prediction == 1)
            
            # Calculate risk factors
            risk_factors = self._identify_risk_factors(
                protocol_type, encryption_used, login_attempts,
                failed_logins, ip_reputation_score, unusual_time_access
            )
            
            return {
                "is_suspicious": is_attack,
                "prediction": "attack" if is_attack else "normal",
                "confidence": confidence,
                "details": {
                    "risk_level": "high" if is_attack and confidence > 0.8 else 
                                  "medium" if is_attack else "low",
                    "protocol": protocol_type,
                    "encryption": encryption_used,
                    "login_attempts": login_attempts,
                    "failed_logins": failed_logins,
                    "ip_reputation": ip_reputation_score,
                    "browser": browser_type,
                    "unusual_time": bool(unusual_time_access),
                    "risk_factors": risk_factors
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error in suspicious access detection: {e}")
            return self._mock_detection(
                network_packet_size, protocol_type, login_attempts,
                session_duration, encryption_used, ip_reputation_score,
                failed_logins, browser_type, unusual_time_access
            )
    
    def _identify_risk_factors(self, protocol_type: str, encryption_used: str,
                               login_attempts: int, failed_logins: int,
                               ip_reputation_score: float, 
                               unusual_time_access: int) -> list:
        """Identify risk factors based on access patterns"""
        risk_factors = []
        
        # Unencrypted or unknown encryption
        if encryption_used.lower() in ['none', 'unknown']:
            risk_factors.append('no_encryption')
        
        # Insecure protocol
        if protocol_type.upper() in ['HTTP', 'FTP', 'TELNET']:
            risk_factors.append('insecure_protocol')
        
        # Multiple login attempts
        if login_attempts > 5:
            risk_factors.append('excessive_login_attempts')
        
        # Failed logins
        if failed_logins > 2:
            risk_factors.append('multiple_failed_logins')
        
        # Low IP reputation
        if ip_reputation_score < 50:
            risk_factors.append('low_ip_reputation')
        
        # Unusual time access
        if unusual_time_access == 1:
            risk_factors.append('unusual_time_access')
        
        return risk_factors
    
    def _mock_detection(self, network_packet_size: int, protocol_type: str,
                       login_attempts: int, session_duration: float,
                       encryption_used: str, ip_reputation_score: float,
                       failed_logins: int, browser_type: str,
                       unusual_time_access: int) -> Dict[str, Any]:
        """Mock detection when model is not available"""
        risk_factors = self._identify_risk_factors(
            protocol_type, encryption_used, login_attempts,
            failed_logins, ip_reputation_score, unusual_time_access
        )
        
        # Calculate score based on risk factors
        score = len(risk_factors)
        
        is_suspicious = score >= 3
        confidence = min(0.5 + (score * 0.1), 0.95)
        
        return {
            "is_suspicious": is_suspicious,
            "prediction": "attack" if is_suspicious else "normal",
            "confidence": confidence,
            "details": {
                "risk_level": "high" if is_suspicious else "low",
                "protocol": protocol_type,
                "encryption": encryption_used,
                "login_attempts": login_attempts,
                "failed_logins": failed_logins,
                "ip_reputation": ip_reputation_score,
                "browser": browser_type,
                "unusual_time": bool(unusual_time_access),
                "risk_factors": risk_factors,
                "mode": "demo"
            }
        }

