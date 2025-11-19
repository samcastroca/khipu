"""
Test del endpoint de suspicious network logs
"""
import requests
import json

# URL del endpoint
url = "http://localhost:8000/api/v1/suspicious-logs/check-log"

# Ejemplos de test basados en el notebook
test_cases = [
    {
        "name": "Conexión normal TCP",
        "data": {
            "duration": 81412.697,
            "proto": "TCP",
            "src_ip_addr": "EXT_SERVER",
            "src_pt": 8082,
            "dst_ip_addr": "OPENSTACK_NET",
            "dst_pt": 56978,
            "packets": 3057,
            "bytes_str": "2.1 M",
            "flags": ".AP..."
        }
    },
    {
        "name": "Posible ataque - muchos paquetes cortos",
        "data": {
            "duration": 0.5,
            "proto": "TCP",
            "src_ip_addr": "UNKNOWN_SERVER",
            "src_pt": 80,
            "dst_ip_addr": "INTERNAL_NET",
            "dst_pt": 443,
            "packets": 5000,
            "bytes_str": "100 K",
            "flags": "S....."
        }
    },
    {
        "name": "Conexión UDP estándar",
        "data": {
            "duration": 120.5,
            "proto": "UDP",
            "src_ip_addr": "LOCAL_SERVER",
            "src_pt": 53,
            "dst_ip_addr": "CLIENT_NET",
            "dst_pt": 53,
            "packets": 250,
            "bytes_str": "50 K",
            "flags": "......"
        }
    },
    {
        "name": "SYN Flood posible",
        "data": {
            "duration": 1.2,
            "proto": "TCP",
            "src_ip_addr": "EXTERNAL_IP",
            "src_pt": 12345,
            "dst_ip_addr": "WEB_SERVER",
            "dst_pt": 80,
            "packets": 10000,
            "bytes_str": "500",
            "flags": "S....."
        }
    }
]

print("=" * 80)
print("🔍 PROBANDO ENDPOINT DE SUSPICIOUS NETWORK LOGS")
print("=" * 80)

for test in test_cases:
    print(f"\n📎 {test['name']}")
    print(f"   Datos:")
    for key, value in test['data'].items():
        print(f"      {key}: {value}")
    
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
