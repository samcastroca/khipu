import joblib
import os
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SuspiciousAccessService:
    """Service for suspicious access detection"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained suspicious access detection model"""
        try:
            if os.path.exists(self.model_path):
                loaded_data = joblib.load(self.model_path)
                
                if isinstance(loaded_data, dict):
                    self.model = loaded_data.get('model')
                else:
                    self.model = loaded_data
                
                logger.info(f"Suspicious access model loaded from {self.model_path}")
            else:
                logger.warning(f"Model file not found: {self.model_path}")
                logger.info("Service will run in mock mode")
        except Exception as e:
            logger.error(f"Error loading suspicious access model: {e}")
            logger.info("Service will run in mock mode")
    
    def check_access(self, user_id: Optional[str], ip_address: str, 
                     timestamp: Optional[str], action: str,
                     location: Optional[str] = None, 
                     device: Optional[str] = None) -> Dict[str, Any]:
        """
        Check if an access attempt is suspicious
        
        Args:
            user_id: User identifier
            ip_address: IP address of the access
            timestamp: Timestamp of the access
            action: Action performed
            location: Geographic location
            device: Device information
            
        Returns:
            Dictionary with detection results
        """
        try:
            if self.model is None:
                return self._mock_detection(user_id, ip_address, timestamp, 
                                           action, location, device)
            
            # Extract features
            features = self._extract_access_features(
                user_id, ip_address, timestamp, action, location, device
            )
            
            # Make prediction
            prediction = self.model.predict([features])[0]
            
            # Get probability if available
            confidence = None
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba([features])[0]
                confidence = float(max(probabilities))
            else:
                confidence = 0.75
            
            is_suspicious = bool(prediction == 1 or prediction == 'suspicious')
            
            return {
                "is_suspicious": is_suspicious,
                "prediction": "suspicious" if is_suspicious else "normal",
                "confidence": confidence,
                "details": self._get_details(is_suspicious, confidence, ip_address, 
                                            location, device, action)
            }
            
        except Exception as e:
            logger.error(f"Error in suspicious access detection: {e}")
            return self._mock_detection(user_id, ip_address, timestamp, 
                                       action, location, device)
    
    def _extract_access_features(self, user_id: Optional[str], ip_address: str,
                                 timestamp: Optional[str], action: str,
                                 location: Optional[str], 
                                 device: Optional[str]) -> list:
        """Extract features from access data"""
        features = []
        
        # IP features
        ip_parts = ip_address.split('.')
        features.extend([int(part) if part.isdigit() else 0 for part in ip_parts[:4]])
        
        # Time features
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                features.extend([dt.hour, dt.weekday()])
            except:
                features.extend([0, 0])
        else:
            features.extend([0, 0])
        
        # Action features
        features.append(1 if 'login' in action.lower() else 0)
        features.append(1 if 'failed' in action.lower() else 0)
        
        # Location features
        features.append(1 if location and location.lower() == 'unknown' else 0)
        
        # Device features
        features.append(1 if device and device.lower() == 'unknown device' else 0)
        
        return features
    
    def _mock_detection(self, user_id: Optional[str], ip_address: str,
                       timestamp: Optional[str], action: str,
                       location: Optional[str], device: Optional[str]) -> Dict[str, Any]:
        """Mock detection when model is not available"""
        anomaly_factors = []
        score = 0
        
        # Check for suspicious patterns
        if location and location.lower() == 'unknown':
            anomaly_factors.append('unknown_location')
            score += 2
        
        if device and device.lower() == 'unknown device':
            anomaly_factors.append('unknown_device')
            score += 2
        
        if 'failed' in action.lower():
            anomaly_factors.append('failed_attempt')
            score += 3
        
        # Check time (if provided)
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                if dt.hour < 6 or dt.hour > 23:
                    anomaly_factors.append('unusual_time')
                    score += 1
            except:
                pass
        
        # Check IP pattern
        if ip_address.startswith('192.168.') or ip_address.startswith('10.'):
            # Private IP - less suspicious
            score -= 1
        else:
            # Public IP - check if it looks unusual
            ip_parts = ip_address.split('.')
            if len(ip_parts) == 4:
                try:
                    first_octet = int(ip_parts[0])
                    if first_octet > 200:
                        anomaly_factors.append('suspicious_ip_range')
                        score += 1
                except:
                    pass
        
        is_suspicious = score >= 3
        confidence = min(0.55 + (score * 0.08), 0.90)
        
        return {
            "is_suspicious": is_suspicious,
            "prediction": "suspicious" if is_suspicious else "normal",
            "confidence": confidence,
            "details": {
                "risk_level": "high" if score >= 5 else "medium" if is_suspicious else "low",
                "anomaly_factors": anomaly_factors,
                "anomaly_score": score,
                "mode": "demo"
            }
        }
    
    def _get_details(self, is_suspicious: bool, confidence: float,
                     ip_address: str, location: Optional[str], 
                     device: Optional[str], action: str) -> Dict[str, Any]:
        """Get additional details about the detection"""
        risk_level = "high" if is_suspicious and confidence > 0.8 else \
                     "medium" if is_suspicious else "low"
        
        anomaly_factors = []
        if is_suspicious:
            if location and location.lower() == 'unknown':
                anomaly_factors.append('unknown_location')
            if device and device.lower() == 'unknown device':
                anomaly_factors.append('unknown_device')
            if 'failed' in action.lower():
                anomaly_factors.append('failed_attempt')
        
        return {
            "risk_level": risk_level,
            "ip_address": ip_address,
            "location": location or "Not provided",
            "device": device or "Not provided",
            "action": action,
            "anomaly_factors": anomaly_factors
        }
