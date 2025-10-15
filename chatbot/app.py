"""
Medical Assistance Chatbot - Flask Web API
RESTful API for the medical chatbot
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import re
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

# Global chatbot instance
chatbot = None

class MedicalAssistantAPI:
    def __init__(self, model_path='medical_chatbot_model.pkl'):
        """Initialize the chatbot with trained model"""
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.symptom_list = model_data['symptom_list']
        self.df_severity = model_data['df_severity']
        self.df_description = model_data['df_description']
        self.df_precaution = model_data['df_precaution']
        self.df_diet = model_data['df_diet']
        
        self.symptom_severity_dict = dict(zip(
            self.df_severity['Symptom'].str.lower().str.replace('_', ' '),
            self.df_severity['weight']
        ))
    
    def normalize_symptom(self, symptom):
        """Normalize symptom name and find closest match"""
        symptom = symptom.lower().strip()
        symptom = re.sub(r'[^\w\s]', '', symptom)
        
        symptom_variants = [
            symptom,
            symptom.replace(' ', '_'),
            symptom.replace('_', ' ')
        ]
        
        for variant in symptom_variants:
            if variant in self.symptom_list:
                return variant
        
        matches = get_close_matches(symptom, self.symptom_list, n=1, cutoff=0.7)
        if matches:
            return matches[0]
        
        symptom_underscore = symptom.replace(' ', '_')
        matches = get_close_matches(symptom_underscore, self.symptom_list, n=1, cutoff=0.7)
        if matches:
            return matches[0]
        
        return None
    
    def predict_disease(self, symptoms, top_n=3):
        """Predict disease based on symptoms"""
        symptom_vector = [0] * len(self.symptom_list)
        
        valid_symptoms = []
        invalid_symptoms = []
        
        for symptom in symptoms:
            normalized = self.normalize_symptom(symptom)
            if normalized:
                valid_symptoms.append(normalized)
                idx = self.symptom_list.index(normalized)
                symptom_vector[idx] = 1
            else:
                invalid_symptoms.append(symptom)
        
        if sum(symptom_vector) == 0:
            return None, valid_symptoms, invalid_symptoms
        
        symptom_vector = np.array(symptom_vector).reshape(1, -1)
        probabilities = self.model.predict_proba(symptom_vector)[0]
        
        top_indices = np.argsort(probabilities)[-top_n:][::-1]
        predictions = []
        
        for idx in top_indices:
            disease = self.model.classes_[idx]
            confidence = probabilities[idx]
            
            predictions.append({
                'disease': disease,
                'confidence': float(confidence * 100),
                'description': self.get_disease_description(disease),
                'precautions': self.get_disease_precautions(disease)
            })
        
        return predictions, valid_symptoms, invalid_symptoms
    
    def get_disease_description(self, disease):
        """Get description of a disease"""
        desc_row = self.df_description[self.df_description['Disease'] == disease]
        if not desc_row.empty:
            return desc_row.iloc[0]['Description']
        return "Description not available."
    
    def get_disease_precautions(self, disease):
        """Get precautions for a disease"""
        prec_row = self.df_precaution[self.df_precaution['Disease'] == disease]
        precautions = []
        
        if not prec_row.empty:
            for col in ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']:
                if col in prec_row.columns:
                    prec = prec_row.iloc[0][col]
                    if pd.notna(prec):
                        precautions.append(prec)
        
        return precautions if precautions else ["Consult a healthcare professional"]
    
    def get_symptom_severity(self, symptoms):
        """Calculate severity score based on symptoms"""
        total_severity = 0
        symptom_severities = []
        
        for symptom in symptoms:
            symptom_clean = symptom.lower().replace('_', ' ')
            severity = self.symptom_severity_dict.get(symptom_clean, 2)
            total_severity += severity
            symptom_severities.append({
                'symptom': symptom,
                'severity': int(severity)
            })
        
        avg_severity = total_severity / len(symptoms) if symptoms else 0
        
        return {
            'total_severity': int(total_severity),
            'average_severity': float(avg_severity),
            'symptom_details': symptom_severities,
            'severity_level': self.get_severity_level(avg_severity)
        }
    
    def get_severity_level(self, avg_severity):
        """Classify severity level"""
        if avg_severity >= 4:
            return "CRITICAL"
        elif avg_severity >= 3:
            return "HIGH"
        elif avg_severity >= 2:
            return "MODERATE"
        else:
            return "LOW"
    
    def get_diet_recommendation(self, chronic_disease=None):
        """Get diet recommendations"""
        if chronic_disease:
            filtered = self.df_diet[self.df_diet['Chronic_Disease'].str.contains(chronic_disease, case=False, na=False)]
            if not filtered.empty:
                sample = filtered.sample(1).iloc[0]
            else:
                sample = self.df_diet.sample(1).iloc[0]
        else:
            sample = self.df_diet.sample(1).iloc[0]
        
        return {
            'meal_plan': sample['Recommended_Meal_Plan'],
            'calories': int(sample['Recommended_Calories']),
            'protein': int(sample['Recommended_Protein']),
            'carbs': int(sample['Recommended_Carbs']),
            'fats': int(sample['Recommended_Fats'])
        }
    
    def get_suggested_symptoms(self, current_symptoms, top_predictions, max_suggestions=8):
        """Suggest additional symptoms to ask about based on top predictions"""
        import pandas as pd
        
        # Get diseases from top predictions
        disease_names = [pred['disease'] for pred in top_predictions]
        
        # Read the disease dataset to find common symptoms for these diseases
        df_disease = pd.read_csv('dataset/dataset.csv')
        
        # Filter for the top predicted diseases
        disease_rows = df_disease[df_disease['Disease'].isin(disease_names)]
        
        # Collect all symptoms from these diseases
        symptom_columns = [col for col in disease_rows.columns if 'Symptom' in col]
        suggested = set()
        
        for _, row in disease_rows.iterrows():
            for col in symptom_columns:
                if pd.notna(row[col]):
                    symptom_string = str(row[col])
                    symptoms = [s.strip() for s in symptom_string.split(',') if s.strip()]
                    suggested.update(symptoms)
        
        # Remove already reported symptoms
        current_symptoms_normalized = [s.lower().replace(' ', '_') for s in current_symptoms]
        suggested = suggested - set(current_symptoms_normalized)
        
        # Remove empty strings
        suggested.discard('')
        
        # Convert to list and format
        suggested_list = [s.replace('_', ' ').title() for s in list(suggested)[:max_suggestions]]
        
        return suggested_list


@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Medical Assistance Chatbot API',
        'version': '1.0',
        'endpoints': {
            '/predict': 'POST - Predict disease from symptoms',
            '/symptoms': 'GET - List all available symptoms',
            '/diseases': 'GET - List all diseases',
            '/health': 'GET - API health check'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': chatbot is not None
    })


@app.route('/symptoms')
def get_symptoms():
    """Get all available symptoms"""
    if chatbot is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'status': 'success',
        'count': len(chatbot.symptom_list),
        'symptoms': [s.replace('_', ' ').title() for s in chatbot.symptom_list]
    })


@app.route('/diseases')
def get_diseases():
    """Get all diseases"""
    if chatbot is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'status': 'success',
        'count': len(chatbot.model.classes_),
        'diseases': list(chatbot.model.classes_)
    })


@app.route('/predict', methods=['POST'])
def predict():
    """Predict disease from symptoms"""
    if chatbot is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if 'symptoms' not in data:
            return jsonify({'error': 'Missing symptoms field'}), 400
        
        symptoms = data['symptoms']
        if isinstance(symptoms, str):
            symptoms = [s.strip() for s in re.split(r'[,;]', symptoms)]
        
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Predict
        predictions, valid_symptoms, invalid_symptoms = chatbot.predict_disease(symptoms, top_n=5)
        
        if predictions is None:
            return jsonify({
                'status': 'error',
                'message': 'No valid symptoms recognized',
                'invalid_symptoms': invalid_symptoms
            }), 400
        
        # Get severity
        severity_info = chatbot.get_symptom_severity(valid_symptoms)
        
        # Check if we have high confidence (>50%)
        max_confidence = predictions[0]['confidence']
        needs_more_symptoms = max_confidence < 50.0
        
        # Get suggested symptoms if confidence is low
        suggested_symptoms = []
        if needs_more_symptoms:
            suggested_symptoms = chatbot.get_suggested_symptoms(valid_symptoms, predictions[:3])
        
        # Get diet recommendation
        top_disease = predictions[0]['disease']
        chronic_diseases = ['Diabetes', 'Hypertension', 'Heart Disease', 'Obesity']
        chronic_match = next((cd for cd in chronic_diseases if cd.lower() in top_disease.lower()), None)
        diet_rec = chatbot.get_diet_recommendation(chronic_disease=chronic_match)
        
        return jsonify({
            'status': 'success',
            'valid_symptoms': [s.replace('_', ' ').title() for s in valid_symptoms],
            'invalid_symptoms': invalid_symptoms,
            'severity': severity_info,
            'predictions': predictions[:3],  # Return top 3
            'needs_more_symptoms': needs_more_symptoms,
            'max_confidence': max_confidence,
            'suggested_symptoms': suggested_symptoms,
            'diet_recommendation': diet_rec,
            'disclaimer': 'This is an AI-based prediction for informational purposes only. Please consult a healthcare professional.'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/disease-info/<disease_name>')
def get_disease_info(disease_name):
    """Get detailed information about a specific disease"""
    if chatbot is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        description = chatbot.get_disease_description(disease_name)
        precautions = chatbot.get_disease_precautions(disease_name)
        
        return jsonify({
            'status': 'success',
            'disease': disease_name,
            'description': description,
            'precautions': precautions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def initialize_chatbot():
    """Initialize the chatbot model"""
    global chatbot
    try:
        print("Loading medical chatbot model...")
        chatbot = MedicalAssistantAPI('medical_chatbot_model.pkl')
        print("✓ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        print("   Please run 'python train_model.py' first to train the model.")


if __name__ == '__main__':
    initialize_chatbot()
    print("\n" + "=" * 60)
    print("🏥 Medical Assistance Chatbot API Server")
    print("=" * 60)
    print("\nServer running at: http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /            - API information")
    print("  GET  /health      - Health check")
    print("  GET  /symptoms    - List all symptoms")
    print("  GET  /diseases    - List all diseases")
    print("  POST /predict     - Predict disease from symptoms")
    print("  GET  /disease-info/<name> - Get disease information")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
