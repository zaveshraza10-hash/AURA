import numpy as np
from sklearn.ensemble import IsolationForest
import pandas as pd
from datetime import datetime

class FraudDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
    
    def train_model(self, historical_data):
        # historical_data: list of dicts with transaction features
        df = pd.DataFrame(historical_data)
        features = ['amount', 'hour_of_day', 'day_of_week', 'transaction_count']
        X = df[features]
        self.model.fit(X)
        self.is_trained = True
    
    def detect(self, transaction):
        if not self.is_trained:
            return {"fraud_probability": 0.0, "is_fraud": False}
        
        features = np.array([[
            transaction['amount'],
            datetime.now().hour,
            datetime.now().weekday(),
            transaction.get('transaction_count', 1)
        ]])
        
        prediction = self.model.predict(features)
        score = self.model.score_samples(features)
        
        is_fraud = prediction[0] == -1
        fraud_prob = 1 / (1 + np.exp(-score[0]))
        
        return {
            "is_fraud": bool(is_fraud),
            "fraud_probability": float(fraud_prob),
            "risk_level": "HIGH" if fraud_prob > 0.7 else "MEDIUM" if fraud_prob > 0.4 else "LOW"
        }