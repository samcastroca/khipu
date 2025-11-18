"""
Script para exportar modelos entrenados desde los notebooks
y guardarlos en el formato correcto para la API
"""
import joblib
import sys
from pathlib import Path


def export_spam_model(model, vectorizer=None, output_path="trained_models/spam_classifier.pkl"):
    """
    Exporta el modelo de clasificación de spam
    
    Args:
        model: El modelo entrenado (ej: LinearSVC, RandomForest, etc.)
        vectorizer: El vectorizador TF-IDF o similar (opcional pero recomendado)
        output_path: Ruta donde guardar el modelo
    """
    try:
        # Crear directorio si no existe
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar modelo y vectorizador juntos
        if vectorizer is not None:
            model_data = {
                'model': model,
                'vectorizer': vectorizer
            }
            joblib.dump(model_data, output_path)
            print(f"✅ Modelo de spam guardado exitosamente en: {output_path}")
            print(f"   - Modelo incluido: {type(model).__name__}")
            print(f"   - Vectorizador incluido: {type(vectorizer).__name__}")
        else:
            # Guardar solo el modelo
            joblib.dump(model, output_path)
            print(f"⚠️  Modelo de spam guardado SIN vectorizador en: {output_path}")
            print(f"   - Modelo incluido: {type(model).__name__}")
            print("   - ADVERTENCIA: Sin vectorizador, el modelo puede no funcionar correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al guardar modelo de spam: {e}")
        return False


def export_phishing_model(model, vectorizer=None, output_path="trained_models/phishing_url_classifier.pkl"):
    """
    Exporta el modelo de detección de phishing
    
    Args:
        model: El modelo entrenado
        vectorizer: El vectorizador (opcional pero recomendado)
        output_path: Ruta donde guardar el modelo
    """
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        if vectorizer is not None:
            model_data = {
                'model': model,
                'vectorizer': vectorizer
            }
            joblib.dump(model_data, output_path)
            print(f"✅ Modelo de phishing guardado exitosamente en: {output_path}")
            print(f"   - Modelo incluido: {type(model).__name__}")
            print(f"   - Vectorizador incluido: {type(vectorizer).__name__}")
        else:
            joblib.dump(model, output_path)
            print(f"⚠️  Modelo de phishing guardado SIN vectorizador en: {output_path}")
            print(f"   - Modelo incluido: {type(model).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al guardar modelo de phishing: {e}")
        return False


def export_suspicious_access_model(model, output_path="trained_models/suspicious_access_classifier.pkl"):
    """
    Exporta el modelo de detección de accesos sospechosos
    
    Args:
        model: El modelo entrenado
        output_path: Ruta donde guardar el modelo
    """
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(model, output_path)
        print(f"✅ Modelo de acceso sospechoso guardado exitosamente en: {output_path}")
        print(f"   - Modelo incluido: {type(model).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al guardar modelo de acceso sospechoso: {e}")
        return False


def verify_model(model_path):
    """
    Verifica que un modelo se pueda cargar correctamente
    
    Args:
        model_path: Ruta al archivo del modelo
    """
    try:
        loaded_data = joblib.load(model_path)
        
        print(f"\n🔍 Verificando modelo: {model_path}")
        
        if isinstance(loaded_data, dict):
            print("   ✓ Formato: Diccionario")
            print(f"   ✓ Claves: {list(loaded_data.keys())}")
            if 'model' in loaded_data:
                print(f"   ✓ Tipo de modelo: {type(loaded_data['model']).__name__}")
            if 'vectorizer' in loaded_data:
                print(f"   ✓ Tipo de vectorizador: {type(loaded_data['vectorizer']).__name__}")
        else:
            print("   ✓ Formato: Objeto directo")
            print(f"   ✓ Tipo: {type(loaded_data).__name__}")
        
        print("   ✅ Modelo verificado correctamente")
        return True
        
    except Exception as e:
        print(f"   ❌ Error al verificar modelo: {e}")
        return False


# Ejemplo de uso:
if __name__ == "__main__":
    print("=" * 60)
    print("Script de Exportación de Modelos para API de Ciberseguridad")
    print("=" * 60)
    print()
    print("⚠️  Este script está diseñado para ser importado desde un notebook")
    print()
    print("Ejemplo de uso en tu notebook:")
    print()
    print("```python")
    print("# Importar el script")
    print("from export_models import export_spam_model")
    print()
    print("# Después de entrenar tu modelo...")
    print("# Exportar modelo de spam")
    print("export_spam_model(")
    print("    model=svm_model,")
    print("    vectorizer=tfidf_vectorizer,")
    print("    output_path='trained_models/spam_classifier.pkl'")
    print(")")
    print()
    print("# Verificar que se guardó correctamente")
    print("from export_models import verify_model")
    print("verify_model('trained_models/spam_classifier.pkl')")
    print("```")
    print()
    print("=" * 60)
