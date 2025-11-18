"""
Script para regenerar el modelo de suspicious access usando datos sintéticos
Este script genera un modelo compatible con sklearn 1.7.2
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
import os

print("=" * 80)
print("🔄 GENERANDO MODELO DE SUSPICIOUS ACCESS (Datos Sintéticos)")
print("=" * 80)

# ---------------------------------------------------
# 1. GENERATE SYNTHETIC DATA
# ---------------------------------------------------
print("\n📊 Generando datos sintéticos...")
np.random.seed(42)
n_samples = 10000

# Generar datos normales (70%)
n_normal = int(n_samples * 0.7)
normal_data = {
    'network_packet_size': np.random.randint(500, 2000, n_normal),
    'protocol_type': np.random.choice(['HTTPS', 'SSH'], n_normal),
    'login_attempts': np.random.randint(1, 3, n_normal),
    'session_duration': np.random.uniform(10, 60, n_normal),
    'encryption_used': np.random.choice(['AES', 'RSA'], n_normal),
    'ip_reputation_score': np.random.uniform(70, 100, n_normal),
    'failed_logins': np.random.randint(0, 1, n_normal),
    'browser_type': np.random.choice(['Chrome', 'Firefox', 'Safari', 'Edge'], n_normal),
    'unusual_time_access': np.random.choice([0], n_normal),
    'attack_detected': 0
}

# Generar datos de ataque (30%)
n_attack = n_samples - n_normal
attack_data = {
    'network_packet_size': np.random.randint(3000, 8000, n_attack),
    'protocol_type': np.random.choice(['HTTP', 'FTP', 'TELNET'], n_attack),
    'login_attempts': np.random.randint(5, 20, n_attack),
    'session_duration': np.random.uniform(0.5, 5, n_attack),
    'encryption_used': np.random.choice(['None', 'Unknown'], n_attack),
    'ip_reputation_score': np.random.uniform(0, 40, n_attack),
    'failed_logins': np.random.randint(3, 15, n_attack),
    'browser_type': np.random.choice(['Unknown', 'Other'], n_attack),
    'unusual_time_access': np.random.choice([1], n_attack),
    'attack_detected': 1
}

# Combinar datasets
df_normal = pd.DataFrame(normal_data)
df_attack = pd.DataFrame(attack_data)
df = pd.concat([df_normal, df_attack], ignore_index=True)

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"   ✅ Dataset generado: {df.shape}")
print(f"   Distribución: Normal={n_normal}, Attack={n_attack}")

# Target & features
X = df.drop("attack_detected", axis=1)
y = df["attack_detected"]

# ---------------------------------------------------
# 2. DEFINE CATEGORICAL & NUMERIC COLUMNS
# ---------------------------------------------------
categorical_cols = ["protocol_type", "encryption_used", "browser_type"]

numeric_cols = [
    "network_packet_size",
    "login_attempts",
    "session_duration",
    "ip_reputation_score",
    "failed_logins",
    "unusual_time_access"
]

print(f"\n📊 Columnas categóricas: {categorical_cols}")
print(f"📊 Columnas numéricas: {numeric_cols}")

# ---------------------------------------------------
# 3. PREPROCESSOR
# ---------------------------------------------------
print("\n🔧 Creando preprocessor...")
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numeric_cols)
    ]
)

# ---------------------------------------------------
# 4. PIPELINE (PREPROCESS + MODEL)
# ---------------------------------------------------
print("🔧 Creando pipeline con GradientBoostingClassifier...")
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", GradientBoostingClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42
    ))
])

# ---------------------------------------------------
# 5. TRAIN / TEST SPLIT
# ---------------------------------------------------
print("\n📦 Dividiendo datos (75/25)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print(f"   Train: {X_train.shape[0]:,} muestras")
print(f"   Test: {X_test.shape[0]:,} muestras")

# ---------------------------------------------------
# 6. TRAIN
# ---------------------------------------------------
print("\n🎯 Entrenando modelo...")
pipeline.fit(X_train, y_train)
print("   ✅ Modelo entrenado")

# ---------------------------------------------------
# 7. EVALUATION
# ---------------------------------------------------
print("\n📈 Evaluando modelo...")
y_pred = pipeline.predict(X_test)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(y_test, y_pred) * 100
precision = precision_score(y_test, y_pred) * 100
recall = recall_score(y_test, y_pred) * 100
f1 = f1_score(y_test, y_pred) * 100

print(f"   Accuracy: {accuracy:.2f}%")
print(f"   Precision: {precision:.2f}%")
print(f"   Recall: {recall:.2f}%")
print(f"   F1-Score: {f1:.2f}%")

# ---------------------------------------------------
# 8. SAVE MODEL
# ---------------------------------------------------
output_path = "../backend/trained_models/suspicious_access_classifier.pkl"
print(f"\n💾 Guardando modelo en: {output_path}")

# Asegurar que el directorio existe
os.makedirs(os.path.dirname(output_path), exist_ok=True)

joblib.dump(pipeline, output_path)
print("   ✅ Modelo guardado exitosamente")

# ---------------------------------------------------
# 9. TEST LOADING
# ---------------------------------------------------
print("\n🧪 Probando carga del modelo...")
loaded_pipeline = joblib.load(output_path)

# Test con muestra normal
sample_normal = pd.DataFrame([{
    'network_packet_size': 1200,
    'protocol_type': 'HTTPS',
    'login_attempts': 1,
    'session_duration': 15.8,
    'encryption_used': 'AES',
    'ip_reputation_score': 85.5,
    'failed_logins': 0,
    'browser_type': 'Chrome',
    'unusual_time_access': 0
}])

pred = loaded_pipeline.predict(sample_normal)[0]
prob = loaded_pipeline.predict_proba(sample_normal)[0]
print(f"   ✅ Modelo cargado correctamente")
print(f"   Predicción acceso normal: {pred} ({'Attack' if pred == 1 else 'Normal'})")
print(f"   Probabilidades: Normal={prob[0]:.4f}, Attack={prob[1]:.4f}")

# Test con muestra de ataque
sample_attack = pd.DataFrame([{
    'network_packet_size': 5000,
    'protocol_type': 'FTP',
    'login_attempts': 15,
    'session_duration': 0.5,
    'encryption_used': 'None',
    'ip_reputation_score': 10.0,
    'failed_logins': 12,
    'browser_type': 'Unknown',
    'unusual_time_access': 1
}])

pred_atk = loaded_pipeline.predict(sample_attack)[0]
prob_atk = loaded_pipeline.predict_proba(sample_attack)[0]
print(f"\n   Predicción acceso ataque: {pred_atk} ({'Attack' if pred_atk == 1 else 'Normal'})")
print(f"   Probabilidades: Normal={prob_atk[0]:.4f}, Attack={prob_atk[1]:.4f}")

print("\n" + "=" * 80)
print("✅ PROCESO COMPLETADO")
print("   El modelo está listo para usarse en el backend")
print("=" * 80)
