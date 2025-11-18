"""
Example script to test the API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_spam_classification():
    """Test spam classification endpoint"""
    print("\n=== Testing Spam Classification ===")
    
    url = f"{BASE_URL}/spam/classify"
    data = {
        "email_text": "Congratulations! You've won $1,000,000. Click here to claim your prize now!"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_phishing_detection():
    """Test phishing URL detection endpoint"""
    print("\n=== Testing Phishing Detection ===")
    
    url = f"{BASE_URL}/phishing/check-url"
    data = {
        "url": "http://suspicious-website.com/login-verify-account"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_suspicious_access():
    """Test suspicious access detection endpoint"""
    print("\n=== Testing Suspicious Access Detection ===")
    
    url = f"{BASE_URL}/suspicious/check-access"
    data = {
        "user_id": "user_123",
        "ip_address": "192.168.1.1",
        "timestamp": "2025-01-15T02:30:00",
        "action": "failed_login_attempt",
        "location": "Unknown",
        "device": "Unknown Device"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_agent_analysis():
    """Test AI agent endpoint"""
    print("\n=== Testing AI Agent ===")
    
    url = f"{BASE_URL}/agent/analyze"
    data = {
        "query": "¿Este correo es spam? 'Get rich quick! Click here now to claim your prize!'",
        "context": {}
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_health_checks():
    """Test all health check endpoints"""
    print("\n=== Testing Health Checks ===")
    
    endpoints = [
        "/spam/health",
        "/phishing/health",
        "/suspicious/health",
        "/agent/health"
    ]
    
    for endpoint in endpoints:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url)
        print(f"\n{endpoint}:")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    print("Testing Cybersecurity API Endpoints")
    print("=" * 50)
    
    try:
        # Test health checks first
        test_health_checks()
        
        # Test individual endpoints
        test_spam_classification()
        test_phishing_detection()
        test_suspicious_access()
        
        # Test agent (requires OpenAI API key)
        # Uncomment if you have OpenAI API key configured
        # test_agent_analysis()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API")
        print("Make sure the server is running: python run.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
