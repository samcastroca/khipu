"""
Script para probar el endpoint de detección de URLs phishing
"""
import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8000/api/v1"

def test_phishing_endpoint():
    """Probar el endpoint de phishing con diferentes URLs"""
    
    # URLs de prueba
    test_urls = [
        # URLs legítimas
        "https://www.google.com",
        "https://www.amazon.com",
        "https://github.com/user/repo",
        "https://www.microsoft.com/support",
        
        # URLs sospechosas/phishing
        "http://paypal-login-free.tk/index.html",
        "http://security-warning-paypal.ga/login.php",
        "http://192.168.1.1/admin/login.php",
        "http://amaz0n-verify-account.com/login",
        "http://www.google.com-verify-login-free.tk/secure",
    ]
    
    print("🔍 PROBANDO ENDPOINT DE PHISHING URLs\n")
    print("=" * 80)
    
    for url in test_urls:
        print(f"\n📎 URL: {url}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/phishing/check-url",
                json={"url": url},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Mostrar resultado
                prediction = data.get("prediction", "").upper()
                confidence = data.get("confidence", 0) * 100
                is_phishing = data.get("is_phishing", False)
                
                emoji = "🚨" if is_phishing else "✅"
                print(f"   {emoji} Predicción: {prediction}")
                print(f"   📊 Confianza: {confidence:.2f}%")
                
                # Mostrar detalles
                details = data.get("details", {})
                if details:
                    risk_level = details.get("risk_level", "unknown")
                    print(f"   ⚠️  Nivel de riesgo: {risk_level.upper()}")
                    
                    risk_factors = details.get("risk_factors", [])
                    if risk_factors:
                        print(f"   🚩 Factores de riesgo: {', '.join(risk_factors)}")
                    
                    if details.get("mode") == "demo":
                        print("   ℹ️  Modo: DEMO (modelo no cargado)")
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Error: No se puede conectar al servidor")
            print("   💡 Asegúrate de que el servidor esté corriendo en http://localhost:8000")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 80)

def test_health():
    """Probar el endpoint de health"""
    print("\n🏥 PROBANDO HEALTH CHECK")
    print("=" * 80)
    
    try:
        response = requests.get(f"{BASE_URL}/phishing/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estado: {data.get('status')}")
            print(f"📝 Servicio: {data.get('service')}")
            print(f"🤖 Modelo: {'Cargado' if data.get('model_loaded') else 'No cargado'}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("💡 Inicia el servidor con: python run.py")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("=" * 80)

if __name__ == "__main__":
    test_health()
    test_phishing_endpoint()
