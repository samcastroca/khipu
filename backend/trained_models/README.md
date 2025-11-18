"""
This directory contains the trained machine learning models.

Expected models:
- spam_classifier.pkl: Spam email classification model
- phishing_url_classifier.pkl: Phishing URL detection model
- suspicious_access_classifier.pkl: Suspicious access detection model

Models should be saved using joblib and can include:
- Just the model object
- A dictionary with 'model' and 'vectorizer' keys

Example of saving a model:
```python
import joblib

# Save model and vectorizer together
model_data = {
    'model': trained_model,
    'vectorizer': tfidf_vectorizer
}
joblib.dump(model_data, 'spam_classifier.pkl')
```
"""
