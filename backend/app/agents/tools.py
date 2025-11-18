from langchain.tools import Tool
from typing import Callable, Dict, Any


def create_spam_classifier_tool(classify_func: Callable) -> Tool:
    """Create a tool for spam classification"""
    
    def spam_wrapper(email_text: str) -> str:
        """Classify an email as spam or legitimate"""
        result = classify_func(email_text)
        return f"Classification: {result['prediction']}, " \
               f"Confidence: {result['confidence']:.2f}, " \
               f"Is Spam: {result['is_spam']}"
    
    return Tool(
        name="spam_classifier",
        func=spam_wrapper,
        description="Useful for classifying emails as spam or legitimate. "
                    "Input should be the email text content. "
                    "Returns whether the email is spam and confidence level."
    )


def create_phishing_url_tool(check_url_func: Callable) -> Tool:
    """Create a tool for phishing URL detection"""
    
    def phishing_wrapper(url: str) -> str:
        """Check if a URL is a phishing attempt"""
        result = check_url_func(url)
        return f"Detection: {result['prediction']}, " \
               f"Confidence: {result['confidence']:.2f}, " \
               f"Is Phishing: {result['is_phishing']}, " \
               f"Risk Level: {result['details']['risk_level']}"
    
    return Tool(
        name="phishing_url_detector",
        func=phishing_wrapper,
        description="Useful for detecting phishing URLs and malicious websites. "
                    "Input should be the URL to check. "
                    "Returns whether the URL is phishing and risk assessment."
    )


def create_suspicious_access_tool(check_access_func: Callable) -> Tool:
    """Create a tool for suspicious access detection"""
    
    def access_wrapper(access_data: str) -> str:
        """Check if an access attempt is suspicious"""
        # Parse the access data string
        # Expected format: "ip:XXX.XXX.XXX.XXX,action:login,location:Unknown"
        data = {}
        for part in access_data.split(','):
            if ':' in part:
                key, value = part.split(':', 1)
                data[key.strip()] = value.strip()
        
        result = check_access_func(
            user_id=data.get('user_id'),
            ip_address=data.get('ip', '0.0.0.0'),
            timestamp=data.get('timestamp'),
            action=data.get('action', 'unknown'),
            location=data.get('location'),
            device=data.get('device')
        )
        
        return f"Detection: {result['prediction']}, " \
               f"Confidence: {result['confidence']:.2f}, " \
               f"Is Suspicious: {result['is_suspicious']}, " \
               f"Risk Level: {result['details']['risk_level']}"
    
    return Tool(
        name="suspicious_access_detector",
        func=access_wrapper,
        description="Useful for detecting suspicious access attempts to systems. "
                    "Input should be access details in format: "
                    "'ip:XXX.XXX.XXX.XXX,action:login_attempt,location:Unknown,device:Chrome'. "
                    "Returns whether the access is suspicious and risk assessment."
    )
