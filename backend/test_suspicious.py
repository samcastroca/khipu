"""
Test del endpoint de suspicious access
"""
import requests
import json

# URL del endpoint
url = "http://localhost:8000/api/v1/suspicious/check-access"

#comentario
# Ejemplos de test basados en el notebook
test_cases = [
    {
        "name": "Acceso normal seguro",
        "data": {
            "network_packet_size": 1200,
            "protocol_type": "HTTPS",
            "login_attempts": 1,
            "session_duration": 15.8,
            "encryption_used": "AES",
            "ip_reputation_score": 85.5,
            "failed_logins": 0,
            "browser_type": "Chrome",
            "unusual_time_access": 0
        }
    },
    {
        "name": "Acceso sospechoso - múltiples intentos fallidos",
        "data": {
            "network_packet_size": 2500,
            "protocol_type": "HTTP",
            "login_attempts": 8,
            "session_duration": 2.3,
            "encryption_used": "None",
            "ip_reputation_score": 25.0,
            "failed_logins": 5,
            "browser_type": "Unknown",
            "unusual_time_access": 1
        }
    },
    {
        "name": "Posible ataque - protocolo inseguro",
        "data": {
            "network_packet_size": 5000,
            "protocol_type": "FTP",
            "login_attempts": 15,
            "session_duration": 0.5,
            "encryption_used": "Unknown",
            "ip_reputation_score": 10.0,
            "failed_logins": 12,
            "browser_type": "Unknown",
            "unusual_time_access": 1
        }
    }
]

print("=" * 80)
print("🔍 PROBANDO ENDPOINT DE SUSPICIOUS ACCESS")
print("=" * 80)

for test in test_cases:
    print(f"\n📎 {test['name']}")
    print(f"   Datos: {json.dumps(test['data'], indent=6)}")
    
    try:
        response = requests.post(
            url,
            json=test['data'],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📊 Resultado:")
            print(json.dumps(result, indent=6, ensure_ascii=False))
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ No se puede conectar al servidor")
        print(f"   💡 Inicia el servidor con: python run.py")
        break
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
