"""
Test rápido con datos sospechosos
"""
import requests
import json

url = "http://localhost:8000/api/v1/suspicious-logs/check-log"

# Ejemplo ALTAMENTE SOSPECHOSO:
# - Duración muy corta (0.5 segundos)
# - Muchos paquetes en poco tiempo (indicador de flooding)
# - Flags solo SYN (posible SYN flood attack)
# - Puerto destino 22 (SSH - posible brute force)
# - IP externa desconocida
suspicious_data = {
    "duration": 0.5,
    "proto": "TCP",
    "src_ip_addr": "UNKNOWN_EXTERNAL",
    "src_pt": 45123,
    "dst_ip_addr": "INTERNAL_SERVER",
    "dst_pt": 22,
    "packets": 15000,
    "bytes_str": "50 K",
    "flags": "S....."
}

print("🚨 PROBANDO EJEMPLO MUY SOSPECHOSO")
print("=" * 80)
print("📊 Datos del ataque:")
print(json.dumps(suspicious_data, indent=2))
print("=" * 80)

try:
    response = requests.post(url, json=suspicious_data)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Respuesta del servidor:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get("is_suspicious"):
            print(f"\n🚨 ALERTA: {result['prediction'].upper()}")
            print(f"💯 Confianza: {result['confidence']*100:.1f}%")
        else:
            print(f"\n✅ Clasificado como: {result['prediction']}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
