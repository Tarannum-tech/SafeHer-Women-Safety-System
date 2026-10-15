import pickle
import pandas as pd
import numpy as np
from pathlib import Path

class SafetyPredictor:
    def __init__(self):
        self.model = None
        self.dataset = None
        self.load_model()
    
    def load_model(self):
        try:
            model_path = Path(__file__).parent.parent / 'model.pkl'
            data_path = Path(__file__).parent.parent / 'data' / 'crime_dataset.csv'
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            self.dataset = pd.read_csv(data_path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict_safety(self, area, time_of_day):
        """Predict safety for a given area and time"""
        area = area.strip().lower()
        
        # Find area in dataset
        row = self.dataset[self.dataset['area'].str.lower() == area]
        
        if row.empty:
            return None, None
        
        crime_count = int(row['crime_count'].values[0])
        is_night = 1 if time_of_day == 'night' else 0
        
        # Predict using model
        result = self.model.predict([[crime_count, is_night]])
        risk = self.model.predict_proba([[crime_count, is_night]])[0][1] * 100
        
        is_safe = result[0] == 0
        return is_safe, risk
    
    def get_area_risk_factors(self, area):
        """Get detailed risk factors for an area"""
        area = area.strip().lower()
        row = self.dataset[self.dataset['area'].str.lower() == area]
        
        if row.empty:
            return None
        
        crime_count = int(row['crime_count'].values[0])
        night_risk = bool(row['night_risk'].values[0])
        
        risk_factors = {
            'crime_count': crime_count,
            'night_risk': night_risk,
            'risk_level': 'High' if crime_count > 15 else 'Medium' if crime_count > 8 else 'Low'
        }
        
        return risk_factors

predictor = SafetyPredictor()