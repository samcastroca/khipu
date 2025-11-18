"""
Script para probar la carga de modelos de phishing directamente
"""
import joblib
from pathlib import Path


def tokenize_url(url: str) -> list:
    """
    Tokeniza una URL separándola en componentes significativos
    Esta función debe estar definida antes de cargar el vectorizador
    """
    # Reemplazar caracteres especiales por espacios
    tokens = url.replace('/', ' ').replace('.', ' ').replace('?', ' ') \
                .replace('=', ' ').replace('&', ' ').replace('-', ' ') \
                .replace('_', ' ').replace(':', ' ')
    # Dividir en tokens
    return tokens.split()


# Rutas de los modelos
model_dir = Path("trained_models")
model_path = model_dir / "phishing_url_logistic_regression.pkl"
vectorizer_path = model_dir / "url_tfidf_vectorizer.pkl"

print("🔍 Verificando archivos de modelos...")
print(f"📂 Directorio: {model_dir.absolute()}")
print(f"🔧 Modelo: {model_path}")
print(f"   Existe: {model_path.exists()}")
print(f"📊 Vectorizer: {vectorizer_path}")
print(f"   Existe: {vectorizer_path.exists()}")

if model_path.exists():
    print(f"\n✅ Cargando modelo desde {model_path}...")
    try:
        model = joblib.load(model_path)
        print(f"   Tipo de modelo: {type(model).__name__}")
        print(f"   Módulo: {type(model).__module__}")
        
        # Intentar obtener algunos atributos del modelo
        if hasattr(model, 'coef_'):
            print(f"   Coeficientes shape: {model.coef_.shape}")
        if hasattr(model, 'classes_'):
            print(f"   Clases: {model.classes_}")
            
    except Exception as e:
        print(f"   ❌ Error cargando modelo: {e}")

if vectorizer_path.exists():
    print(f"\n✅ Cargando vectorizador desde {vectorizer_path}...")
    try:
        vectorizer = joblib.load(vectorizer_path)
        print(f"   Tipo: {type(vectorizer).__name__}")
        print(f"   Módulo: {type(vectorizer).__module__}")
        
        # Intentar obtener algunos atributos
        if hasattr(vectorizer, 'vocabulary_'):
            print(f"   Vocabulario size: {len(vectorizer.vocabulary_)}")
        if hasattr(vectorizer, 'max_features'):
            print(f"   Max features: {vectorizer.max_features}")
        if hasattr(vectorizer, 'lowercase'):
            print(f"   Lowercase: {vectorizer.lowercase}")
            
    except Exception as e:
        print(f"   ❌ Error cargando vectorizador: {e}")

# Probar una predicción
if model_path.exists() and vectorizer_path.exists():
    print("\n🧪 PROBANDO PREDICCIÓN:")
    print("=" * 60)
    
    test_urls = [
        "https://www.google.com",
        "http://paypal-login-free.tk/index.html",
        "http://192.168.1.1/admin/login.php"
    ]
    
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        
        for url in test_urls:
            # Vectorizar
            url_vector = vectorizer.transform([url])
            
            # Predecir
            prediction = model.predict(url_vector)[0]
            probabilities = model.predict_proba(url_vector)[0]
            
            # Interpretar
            is_phishing = bool(prediction == 1)
            confidence = float(probabilities[1] if is_phishing else probabilities[0])
            
            emoji = "🚨" if is_phishing else "✅"
            label = "PHISHING" if is_phishing else "LEGÍTIMA"
            
            print(f"{emoji} {label} ({confidence*100:.1f}%): {url}")
            
    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        import traceback
        traceback.print_exc()
