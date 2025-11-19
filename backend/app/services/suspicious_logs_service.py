import joblib
import os
from typing import Dict, Any
import logging
import pandas as pd
import re

logger = logging.getLogger(__name__)


class SuspiciousLogsService:
    """Service for suspicious network logs detection using DecisionTree"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained suspicious logs detection pipeline"""
        try:
            if os.path.exists(self.model_path):
                self.pipeline = joblib.load(self.model_path)
                logger.info(f"✅ Suspicious logs pipeline loaded from {self.model_path}")
            else:
                logger.warning(f"⚠️  Model file not found: {self.model_path}")
                logger.info("Service will run in mock mode")
        except Exception as e:
            logger.error(f"❌ Error loading suspicious logs model: {e}")
            logger.info("Service will run in mock mode")
    
    def check_log(self,
                  duration: float,
                  proto: str,
                  src_ip_addr: str,
                  src_pt: int,
                  dst_ip_addr: str,
                  dst_pt: float,
                  packets: int,
                  bytes_str: str,
                  flags: str) -> Dict[str, Any]:
        """
        Check if a network log is suspicious/attack
        
        Args:
            duration: Duration of connection
            proto: Protocol (TCP, UDP, ICMP, etc.)
            src_ip_addr: Source IP address identifier
            src_pt: Source port
            dst_ip_addr: Destination IP address identifier
            dst_pt: Destination port
            packets: Number of packets
            bytes_str: Bytes transferred (e.g., "2.1 M", "500 K", "1234")
            flags: TCP flags (e.g., ".AP...", "S.....", etc.)
            
        Returns:
            Dictionary with detection results
        """
        try:
            if self.pipeline is None:
                return self._mock_detection(
                    duration, proto, src_ip_addr, src_pt,
                    dst_ip_addr, dst_pt, packets, bytes_str, flags
                )
            
            # Extract model components
            model = self.pipeline["model"]
            encoders = self.pipeline["encoders"]
            features = self.pipeline["features"]
            set_flag = self.pipeline["set_flag"]
            # Don't use conv_bytes from pipeline, use our own
            
            # Create sample DataFrame
            sample = {
                "Duration": float(duration),
                "Proto": str(proto),
                "Src IP Addr": str(src_ip_addr),
                "Src Pt": int(src_pt),
                "Dst IP Addr": str(dst_ip_addr),
                "Dst Pt": float(dst_pt),
                "Packets": int(packets),
                "Bytes": str(bytes_str),
                "Flags": str(flags)
            }
            
            df = pd.DataFrame([sample])
            
            # Add flag columns
            for flag in ["A", "P", "S", "R", "F", "x"]:
                df[flag] = df.apply(lambda r: set_flag(r, flag), axis=1)
            
            # Convert Bytes manually - don't use conv_bytes from pipeline
            def convert_bytes_str(val):
                if pd.isna(val):
                    return 0.0
                val = str(val).strip()
                if "M" in val.upper():
                    num = re.findall(r"[0-9.]+", val)
                    return float("".join(num)) * 1_000_000 if num else 0.0
                elif "K" in val.upper():
                    num = re.findall(r"[0-9.]+", val)
                    return float("".join(num)) * 1_000 if num else 0.0
                else:
                    try:
                        return float(val)
                    except:
                        return 0.0
            
            df["Bytes"] = df["Bytes"].apply(convert_bytes_str)
            
            # Apply encoders
            for col in ["Proto", "Src IP Addr", "Dst IP Addr"]:
                if col in df.columns:
                    df[col] = df[col].astype(str).map(
                        lambda x: encoders[col].transform([x])[0] 
                        if x in encoders[col].classes_ else -1
                    )
            
            # Ensure same column order as training
            df = df.reindex(columns=features, fill_value=0)
            
            # Make prediction
            prediction = model.predict(df)[0]
            
            # Get probability if available
            confidence = None
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(df)[0]
                confidence = float(probabilities[prediction])
            else:
                confidence = 0.85
            
            # Decode class label
            class_label = encoders['class'].inverse_transform([prediction])[0]
            is_attack = (class_label != 'normal' and class_label != 'benign')
            
            # Extract flag details
            flag_details = self._extract_flag_details(flags)
            
            return {
                "is_suspicious": is_attack,
                "prediction": class_label,
                "confidence": confidence,
                "details": {
                    "risk_level": "high" if is_attack and confidence > 0.8 else 
                                  "medium" if is_attack else "low",
                    "protocol": proto,
                    "source": f"{src_ip_addr}:{src_pt}",
                    "destination": f"{dst_ip_addr}:{dst_pt}",
                    "packets": packets,
                    "bytes": bytes_str,
                    "duration": duration,
                    "flags": flag_details
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error in suspicious logs detection: {e}")
            return self._mock_detection(
                duration, proto, src_ip_addr, src_pt,
                dst_ip_addr, dst_pt, packets, bytes_str, flags
            )
    
    def _extract_flag_details(self, flags: str) -> Dict[str, bool]:
        """Extract TCP flag details"""
        return {
            "ACK": "A" in flags,
            "PSH": "P" in flags,
            "SYN": "S" in flags,
            "RST": "R" in flags,
            "FIN": "F" in flags,
            "URG": "x" in flags
        }
    
    def _mock_detection(self, duration: float, proto: str,
                       src_ip_addr: str, src_pt: int,
                       dst_ip_addr: str, dst_pt: float,
                       packets: int, bytes_str: str,
                       flags: str) -> Dict[str, Any]:
        """Mock detection when model is not available"""
        risk_factors = []
        score = 0
        
        # Check for suspicious patterns
        if packets > 1000:
            risk_factors.append('high_packet_count')
            score += 2
        
        if duration < 1.0 and packets > 100:
            risk_factors.append('short_duration_high_packets')
            score += 2
        
        if proto.upper() not in ['TCP', 'UDP', 'ICMP']:
            risk_factors.append('unusual_protocol')
            score += 1
        
        # Check flags
        if 'S' in flags and 'A' not in flags:
            risk_factors.append('syn_without_ack')
            score += 1
        
        is_suspicious = score >= 3
        confidence = min(0.5 + (score * 0.1), 0.95)
        
        flag_details = self._extract_flag_details(flags)
        
        return {
            "is_suspicious": is_suspicious,
            "prediction": "suspicious" if is_suspicious else "normal",
            "confidence": confidence,
            "details": {
                "risk_level": "high" if is_suspicious else "low",
                "protocol": proto,
                "source": f"{src_ip_addr}:{src_pt}",
                "destination": f"{dst_ip_addr}:{dst_pt}",
                "packets": packets,
                "bytes": bytes_str,
                "duration": duration,
                "flags": flag_details,
                "risk_factors": risk_factors,
                "mode": "demo"
            }
        }
