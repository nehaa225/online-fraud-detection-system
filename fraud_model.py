import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

MODEL_PATH = "fraud_model.pkl"
VECTORIZER_PATH = "tfidf_vectorizer.pkl"
DATA_PATH = "dataset.csv"

def train_model():
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return False
        
    df = pd.read_csv(DATA_PATH)
    
    X = df['text']
    y = df['label'] # 'Fraud' or 'Safe'
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_vec = vectorizer.fit_transform(X)
    
    model = LogisticRegression()
    model.fit(X_vec, y)
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print("Model and vectorizer trained and saved successfully.")
    return True

def predict_fraud(text):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("Model not found. Training now...")
        success = train_model()
        if not success:
            return "Error", 0.0
            
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    
    probabilities = model.predict_proba(text_vec)[0]
    class_index = list(model.classes_).index(prediction)
    confidence = probabilities[class_index] * 100
    
    return prediction, confidence

if __name__ == "__main__":
    train_model()
