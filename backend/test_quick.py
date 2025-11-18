"""
Script rápido para probar la API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("🔬 Probando API de Ciberseguridad")
print("=" * 60)

# Test 1: Spam Classification
print("\n\n1️⃣ Clasificación de Spam")
print("-" * 40)

email_spam = "Congratulations! You've won $1,000,000. Click here to claim your prize now!"
response = requests.post(
    f"{BASE_URL}/spam/classify",
    json={"email_text": email_spam}
)

print(f"📧 Email: {email_spam[:50]}...")
print(f"✅ Status: {response.status_code}")
result = response.json()
print(f"🎯 Resultado: {json.dumps(result, indent=2)}")

#Test 2: Email Legítimo
print("\n\n2️⃣ Email Legítimo")
print("-" * 40)

email_legit = "Hi John, can we schedule a meeting tomorrow at 3pm to discuss the project requirements?"
response = requests.post(
    f"{BASE_URL}/spam/classify",
    json={"email_text": email_legit}
)

print(f"📧 Email: {email_legit[:50]}...")
print(f"✅ Status: {response.status_code}")
result = response.json()
print(f"🎯 Resultado: {json.dumps(result, indent=2)}")

print("\n\n" + "=" * 60)
print("✅ Prueba completada!")
print("=" * 60)
