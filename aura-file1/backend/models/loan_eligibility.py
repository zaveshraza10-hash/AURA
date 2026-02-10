import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class LoanPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.load_model()
    
    def load_model(self):
        try:
            with open("ai_models/loan_model.pkl", "rb") as f:
                self.model = pickle.load(f)
            with open("ai_models/scaler.pkl", "rb") as f:
                self.scaler = pickle.load(f)
        except:
            self.train_model()
    
    def train_model(self):
        # Synthetic data
        np.random.seed(42)
        n_samples = 1000
        data = {
            'age': np.random.randint(20, 60, n_samples),
            'income': np.random.randint(20000, 150000, n_samples),
            'credit_score': np.random.randint(300, 850, n_samples),
            'existing_loans': np.random.randint(0, 5, n_samples),
            'account_balance': np.random.randint(1000, 100000, n_samples),
            'employment_years': np.random.randint(0, 30, n_samples)
        }
        df = pd.DataFrame(data)
        df['loan_amount'] = np.random.randint(5000, 50000, n_samples)
        df['eligible'] = ((df['income'] > 30000) & 
                         (df['credit_score'] > 600) & 
                         (df['existing_loans'] < 3)).astype(int)
        
        X = df.drop('eligible', axis=1)
        y = df['eligible']
        
        X_scaled = self.scaler.fit_transform(X)
        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X_scaled, y)
        
        # Save models
        with open("ai_models/loan_model.pkl", "wb") as f:
            pickle.dump(self.model, f)
        with open("ai_models/scaler.pkl", "wb") as f:
            pickle.dump(self.scaler, f)
    
    def predict(self, user_data):
        df = pd.DataFrame([user_data])
        scaled = self.scaler.transform(df)
        prob = self.model.predict_proba(scaled)[0][1]
        eligible = prob > 0.6
        return {
            "eligible": bool(eligible),
            "probability": float(prob),
            "suggested_limit": user_data['income'] * 0.5 if eligible else 0,
            "interest_rate": 12.5 if prob > 0.8 else 15.0
        }