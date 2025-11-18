"""
Script para entrenar el modelo de suspicious access con la versión correcta de sklearn
"""
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import os

print("=" * 80)
print("🔄 ENTRENANDO MODELO DE SUSPICIOUS ACCESS")
print("=" * 80)

# ---------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------
print("\n📂 Cargando datos...")
df = pd.read_csv("cybersecurity_intrusion_data.csv")
print(f"   ✅ Dataset cargado: {df.shape}")

# Fix missing categorical values
df["encryption_used"] = df["encryption_used"].fillna("Unknown")

# Drop session_id (irrelevant for ML)
df = df.drop("session_id", axis=1)

# Target & features
X = df.drop("attack_detected", axis=1)
y = df["attack_detected"]

print(f"   Features: {list(X.columns)}")
print(f"   Target: attack_detected")
print(f"   Distribución: {y.value_counts().to_dict()}")

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
    ("model", GradientBoostingClassifier(random_state=42))
])

# ---------------------------------------------------
# 5. TRAIN / TEST SPLIT
# ---------------------------------------------------
print("\n📦 Dividiendo datos (75/25)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
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

accuracy = accuracy_score(y_test, y_pred) * 100
precision = precision_score(y_test, y_pred) * 100
recall = recall_score(y_test, y_pred) * 100

print(f"   Accuracy: {accuracy:.2f}%")
print(f"   Precision: {precision:.2f}%")
print(f"   Recall: {recall:.2f}%")

# ---------------------------------------------------
# 8. SAVE MODEL
# ---------------------------------------------------
output_path = "../backend/trained_models/suspicious_access_classifier.pkl"
print(f"\n💾 Guardando modelo en: {output_path}")
joblib.dump(pipeline, output_path)
print("   ✅ Modelo guardado exitosamente")

# ---------------------------------------------------
# 9. TEST LOADING
# ---------------------------------------------------
print("\n🧪 Probando carga del modelo...")
loaded_pipeline = joblib.load(output_path)
test_sample = X_test.iloc[0:1]
test_pred = loaded_pipeline.predict(test_sample)[0]
test_prob = loaded_pipeline.predict_proba(test_sample)[0]
print(f"   ✅ Modelo cargado correctamente")
print(f"   Predicción de prueba: {test_pred} (prob: {test_prob})")

print("\n" + "=" * 80)
print("✅ PROCESO COMPLETADO")
print("=" * 80)
