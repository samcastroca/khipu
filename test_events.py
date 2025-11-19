import requests
import json
from datetime import datetime
import time

# Configuration
BASE_URL = "http://khipu.vercel.app"
EVENTS_ENDPOINT = f"{BASE_URL}/api/events/ingest"

def send_event(name, event_type, data, description):
    """Send a single event with description"""
    print(f"\n{'='*70}")
    print(f"📋 {name}")
    print(f"   {description}")
    print(f"{'='*70}")
    
    payload = {
        "type": event_type,
        "data": data
    }
    
    # Show what we're sending
    print(f"📤 Enviando:")
    for key, value in data.items():
        print(f"   {key}: {value}")
    
    try:
        response = requests.post(EVENTS_ENDPOINT, json=payload)
        print(f"\n📥 Respuesta: Status {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                event = result.get('event', {})
                confidence_pct = float(event.get('confidence', 0)) * 100
                is_threat = event.get('isThreat')
                severity = event.get('severity', 'unknown').upper()
                
                threat_icon = "🔴" if is_threat else "🟢"
                print(f"✅ Resultado: {threat_icon} {'AMENAZA' if is_threat else 'NORMAL'}")
                print(f"   Severidad: {severity}")
                print(f"   Confianza: {confidence_pct:.2f}%")
                
                return event
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    time.sleep(2)
    return None

def demo_network_access():
    """Demonstrate network access scenarios with different threat levels"""
    print("\n" + "="*70)
    print("🔐 DEMOSTRACIÓN: ANÁLISIS DE ACCESOS DE RED")
    print("="*70)
    
    scenarios = [
        {
            "name": "Escenario 1: Acceso Corporativo Normal",
            "description": "Usuario legítimo con navegador Chrome, HTTPS, sin intentos fallidos",
            "data": {
                "network_packet_size": 1200,
                "protocol_type": "HTTPS",
                "login_attempts": 1,
                "session_duration": 45,
                "encryption_used": "TLS",
                "ip_reputation_score": 95,
                "failed_logins": 0,
                "browser_type": "Chrome",
                "unusual_time_access": 0
            }
        },
        {
            "name": "Escenario 2: Acceso Sospechoso Leve",
            "description": "Navegador desconocido, horario inusual, pero con encriptación",
            "data": {
                "network_packet_size": 1800,
                "protocol_type": "HTTP",
                "login_attempts": 3,
                "session_duration": 120,
                "encryption_used": "TLS",
                "ip_reputation_score": 45,
                "failed_logins": 1,
                "browser_type": "Unknown",
                "unusual_time_access": 1
            }
        },
        {
            "name": "Escenario 3: Ataque de Fuerza Bruta",
            "description": "Múltiples intentos fallidos, sin encriptación, IP sospechosa",
            "data": {
                "network_packet_size": 800,
                "protocol_type": "SSH",
                "login_attempts": 15,
                "session_duration": 5,
                "encryption_used": "None",
                "ip_reputation_score": 10,
                "failed_logins": 14,
                "browser_type": "Bot",
                "unusual_time_access": 1
            }
        },
        {
            "name": "Escenario 4: Intento de Exfiltración",
            "description": "Paquetes grandes, sesión larga, protocolo FTP sin encriptación",
            "data": {
                "network_packet_size": 9000,
                "protocol_type": "FTP",
                "login_attempts": 1,
                "session_duration": 240,
                "encryption_used": "None",
                "ip_reputation_score": 25,
                "failed_logins": 0,
                "browser_type": "Unknown",
                "unusual_time_access": 1
            }
        },
        {
            "name": "Escenario 5: Acceso Privilegiado Normal",
            "description": "Admin legítimo con SSH seguro, buena reputación IP",
            "data": {
                "network_packet_size": 1500,
                "protocol_type": "SSH",
                "login_attempts": 1,
                "session_duration": 30,
                "encryption_used": "AES",
                "ip_reputation_score": 90,
                "failed_logins": 0,
                "browser_type": "Terminal",
                "unusual_time_access": 0
            }
        }
    ]
    
    for scenario in scenarios:
        send_event(
            scenario["name"],
            "network_access",
            scenario["data"],
            scenario["description"]
        )

def demo_suspicious_logs():
    """Demonstrate network log scenarios with different attack patterns"""
    print("\n" + "="*70)
    print("🌐 DEMOSTRACIÓN: ANÁLISIS DE LOGS DE RED")
    print("="*70)
    
    scenarios = [
        {
            "name": "Escenario 1: Tráfico HTTPS Legítimo",
            "description": "Conexión normal a servidor web seguro, flags completos",
            "data": {
                "duration": "2.5",
                "proto": "tcp",
                "src_ip_addr": "192.168.1.50",
                "src_pt": "49152",
                "dst_ip_addr": "93.184.216.34",
                "dst_pt": "443",
                "packets": "25",
                "bytes_str": "12500",
                "flags": "FPSRA"
            }
        },
        {
            "name": "Escenario 2: SYN Flood - Ataque DDoS",
            "description": "Miles de paquetes SYN sin ACK, duración mínima, indica flooding",
            "data": {
                "duration": "0.000001",
                "proto": "tcp",
                "src_ip_addr": "203.0.113.100",
                "src_pt": "54321",
                "dst_ip_addr": "10.0.0.1",
                "dst_pt": "80",
                "packets": "5000",
                "bytes_str": "250000",
                "flags": "S"
            }
        },
        {
            "name": "Escenario 3: Port Scan Detected",
            "description": "Escaneo de puertos, 1 paquete por conexión, múltiples puertos",
            "data": {
                "duration": "0.001",
                "proto": "tcp",
                "src_ip_addr": "198.51.100.50",
                "src_pt": "12345",
                "dst_ip_addr": "192.168.1.1",
                "dst_pt": "22",
                "packets": "1",
                "bytes_str": "40",
                "flags": "S"
            }
        },
        {
            "name": "Escenario 4: Transferencia SSH Normal",
            "description": "Sesión SSH legítima con transferencia de datos moderada",
            "data": {
                "duration": "3.8",
                "proto": "tcp",
                "src_ip_addr": "192.168.1.10",
                "src_pt": "50123",
                "dst_ip_addr": "10.0.0.5",
                "dst_pt": "22",
                "packets": "150",
                "bytes_str": "75000",
                "flags": "PA"
            }
        },
        {
            "name": "Escenario 5: UDP Flood Attack",
            "description": "Ataque de inundación UDP, muchos paquetes pequeños",
            "data": {
                "duration": "0.0005",
                "proto": "udp",
                "src_ip_addr": "185.220.101.50",
                "src_pt": "19234",
                "dst_ip_addr": "10.0.0.1",
                "dst_pt": "53",
                "packets": "3000",
                "bytes_str": "90000",
                "flags": ""
            }
        },
        {
            "name": "Escenario 6: Data Exfiltration Attempt",
            "description": "Transferencia sospechosa de gran volumen de datos",
            "data": {
                "duration": "0.8",
                "proto": "tcp",
                "src_ip_addr": "172.16.0.25",
                "src_pt": "48765",
                "dst_ip_addr": "198.18.0.100",
                "dst_pt": "8080",
                "packets": "1200",
                "bytes_str": "2.5 M",
                "flags": "PA"
            }
        },
        {
            "name": "Escenario 7: DNS Query Normal",
            "description": "Consulta DNS legítima, protocolo UDP estándar",
            "data": {
                "duration": "0.05",
                "proto": "udp",
                "src_ip_addr": "192.168.1.25",
                "src_pt": "52341",
                "dst_ip_addr": "8.8.8.8",
                "dst_pt": "53",
                "packets": "2",
                "bytes_str": "128",
                "flags": ""
            }
        },
        {
            "name": "Escenario 8: ACK Flood Attack",
            "description": "Flood de paquetes ACK sin contexto de conexión",
            "data": {
                "duration": "0.0002",
                "proto": "tcp",
                "src_ip_addr": "45.142.120.80",
                "src_pt": "35789",
                "dst_ip_addr": "10.0.0.1",
                "dst_pt": "443",
                "packets": "2500",
                "bytes_str": "125000",
                "flags": "A"
            }
        }
    ]
    
    for scenario in scenarios:
        send_event(
            scenario["name"],
            "suspicious_logs",
            scenario["data"],
            scenario["description"]
        )

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎯 KHIPU CYBERSECURITY - DEMOSTRACIÓN DE ANÁLISIS ML")
    print("="*70)
    print(f"🕐 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Objetivo: Demostrar diferentes niveles de amenaza detectados por ML")
    print(f"📊 Endpoint: {EVENTS_ENDPOINT}")
    print("="*70)
    
    start_time = time.time()
    
    try:
        # Demo de accesos de red (5 escenarios)
        demo_network_access()
        
        print("\n⏸️  Pausa de 3 segundos entre fases...")
        time.sleep(3)
        
        # Demo de logs de red (8 escenarios)
        demo_suspicious_logs()
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "="*70)
        print("✅ DEMOSTRACIÓN COMPLETADA")
        print("="*70)
        print(f"⏱️  Tiempo total: {elapsed_time:.1f} segundos")
        print(f"📊 Total de eventos: 13 (5 accesos + 8 logs)")
        print(f"🌐 Dashboard: {BASE_URL}")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()
