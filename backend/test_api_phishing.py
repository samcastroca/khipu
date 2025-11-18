"""
Test simple del endpoint de phishing
"""
import requests
import json

# URL del endpoint
url = "http://localhost:8000/api/v1/phishing/url"

# Tests
test_cases = [
    "http://paypal-login-free.tk/index.html",
    "https://www.google.com",
    "pkbsurf.com.br/aolfile010/570d3e49c6bc9b64a84c1d02093ad580/"
]

print("=" * 80)
print("🔍 PROBANDO ENDPOINT DE PHISHING URLs")
print("=" * 80)

for test_url in test_cases:
    print(f"\n📎 Testeando: {test_url}")
    
    try:
        response = requests.post(
            url,
            json={"url": test_url},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📊 Resultado:")
            print(json.dumps(result, indent=4, ensure_ascii=False))
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ No se puede conectar al servidor")
        print(f"   💡 Inicia el servidor con: python run.py")
        break
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
