"""
Script simple para probar un solo URL
"""
import joblib

def tokenize_url(url):
    tokens = url.replace('/', ' ').replace('.', ' ').replace('?', ' ') \
                .replace('=', ' ').replace('&', ' ').replace('-', ' ') \
                .replace('_', ' ').replace(':', ' ')
    return tokens.split()

model = joblib.load('trained_models/phishing_url_logistic_regression.pkl')
vectorizer = joblib.load('trained_models/url_tfidf_vectorizer.pkl')

# Test con Google
url = 'https://www.google.com'
vec = vectorizer.transform([url])
pred = model.predict(vec)[0]
prob = model.predict_proba(vec)[0]

# Model labels (as shown in notebook): 0 = legitimate (good), 1 = phishing (bad)
is_phishing = (pred == 1)
label = "PHISHING" if is_phishing else "LEGÍTIMA"
# Use probability of predicted class
conf = prob[0] if pred == 0 else prob[1]

print(f'URL: {url}')
print(f'Prediction raw: {pred}')
print(f'Label: {label}')
print(f'Confidence: {conf:.4f}')
print(f'Probabilities: {prob}')

# Test con URL phishing
url2 = 'http://paypal-login-free.tk/index.html'
vec2 = vectorizer.transform([url2])
pred2 = model.predict(vec2)[0]
prob2 = model.predict_proba(vec2)[0]

is_phishing2 = (pred2 == 1)
label2 = "PHISHING" if is_phishing2 else "LEGÍTIMA"
conf2 = prob2[0] if pred2 == 0 else prob2[1]

print(f'\nURL: {url2}')
print(f'Prediction raw: {pred2}')
print(f'Label: {label2}')
print(f'Confidence: {conf2:.4f}')
print(f'Probabilities: {prob2}')
