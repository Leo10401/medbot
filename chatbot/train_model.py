"""
Medical Assistance Chatbot - Model Training Script
This script trains a machine learning model to predict diseases based on symptoms
and integrates multiple medical datasets for comprehensive assistance.
"""

import pandas as pd
import numpy as np
import pickle
import warnings
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
import re

warnings.filterwarnings('ignore')

class MedicalChatbotModel:
    def __init__(self, dataset_path='dataset/'):
        self.dataset_path = dataset_path
        self.disease_model = None
        self.label_encoder = None
        self.symptom_list = []
        
        # Load all datasets
        self.load_datasets()
        
    def load_datasets(self):
        """Load all medical datasets"""
        print("Loading datasets...")
        
        # Main disease-symptom dataset
        self.df_disease = pd.read_csv(f'{self.dataset_path}dataset.csv')
        
        # Symptom severity
        self.df_severity = pd.read_csv(f'{self.dataset_path}Symptom-severity.csv')
        
        # Disease descriptions
        self.df_description = pd.read_csv(f'{self.dataset_path}symptom_Description.csv')
        
        # Disease precautions
        self.df_precaution = pd.read_csv(f'{self.dataset_path}symptom_precaution.csv')
        
        # Diet recommendations
        self.df_diet = pd.read_csv(f'{self.dataset_path}Personalized_Diet_Recommendations.csv')
        
        print(f"✓ Loaded {len(self.df_disease)} disease records")
        print(f"✓ Loaded {len(self.df_severity)} symptom severity records")
        print(f"✓ Loaded {len(self.df_description)} disease descriptions")
        print(f"✓ Loaded {len(self.df_precaution)} precaution records")
        print(f"✓ Loaded {len(self.df_diet)} diet recommendation records")
        
    def preprocess_disease_data(self):
        """Preprocess the disease-symptom dataset"""
        print("\nPreprocessing disease-symptom data...")
        
        # Extract all symptoms from the dataset
        symptom_columns = [col for col in self.df_disease.columns if 'Symptom' in col]
        
        # Collect all unique symptoms
        all_symptoms = set()
        for col in symptom_columns:
            symptoms = self.df_disease[col].dropna().astype(str)
            for symptom_string in symptoms:
                # Split by comma and clean
                symptom_parts = [s.strip() for s in symptom_string.split(',') if s.strip()]
                all_symptoms.update(symptom_parts)
        
        # Remove empty strings
        all_symptoms.discard('')
        self.symptom_list = sorted(list(all_symptoms))
        
        print(f"✓ Found {len(self.symptom_list)} unique symptoms")
        
        # Create feature matrix
        X = []
        y = []
        
        for idx, row in self.df_disease.iterrows():
            disease = row['Disease']
            # Create binary vector for symptoms
            symptom_vector = [0] * len(self.symptom_list)
            
            for col in symptom_columns:
                if pd.notna(row[col]):
                    symptom_string = str(row[col])
                    symptoms = [s.strip() for s in symptom_string.split(',') if s.strip()]
                    
                    for symptom in symptoms:
                        if symptom in self.symptom_list:
                            symptom_idx = self.symptom_list.index(symptom)
                            symptom_vector[symptom_idx] = 1
            
            # Only add if at least one symptom is present
            if sum(symptom_vector) > 0:
                X.append(symptom_vector)
                y.append(disease)
        
        self.X = np.array(X)
        self.y = np.array(y)
        
        print(f"✓ Created feature matrix with shape: {self.X.shape}")
        print(f"✓ Number of diseases: {len(set(y))}")
        
        return self.X, self.y
    
    def train_models(self):
        """Train multiple models and select the best one"""
        print("\nTraining models...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        # Define models to train
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5),
            'SVM': SVC(kernel='rbf', probability=True, random_state=42)
        }
        
        best_model = None
        best_score = 0
        best_name = ""
        
        for name, model in models.items():
            print(f"\nTraining {name}...")
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            cv_mean = cv_scores.mean()
            
            print(f"  Test Accuracy: {accuracy:.4f}")
            print(f"  CV Score: {cv_mean:.4f} (+/- {cv_scores.std():.4f})")
            
            if accuracy > best_score:
                best_score = accuracy
                best_model = model
                best_name = name
        
        self.disease_model = best_model
        print(f"\n✓ Best model: {best_name} with accuracy {best_score:.4f}")
        
        # Final evaluation
        y_pred_final = self.disease_model.predict(X_test)
        print("\nFinal Model Performance:")
        print(classification_report(y_test, y_pred_final))
        
        return self.disease_model
    
    def save_model(self, filename='medical_chatbot_model.pkl'):
        """Save the trained model and associated data"""
        print(f"\nSaving model to {filename}...")
        
        model_data = {
            'model': self.disease_model,
            'symptom_list': self.symptom_list,
            'df_severity': self.df_severity,
            'df_description': self.df_description,
            'df_precaution': self.df_precaution,
            'df_diet': self.df_diet
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✓ Model saved successfully!")
    
    def get_disease_info(self, disease):
        """Get comprehensive information about a disease"""
        info = {
            'disease': disease,
            'description': None,
            'precautions': [],
            'severity': 0
        }
        
        # Get description
        desc_row = self.df_description[self.df_description['Disease'] == disease]
        if not desc_row.empty:
            info['description'] = desc_row.iloc[0]['Description']
        
        # Get precautions
        prec_row = self.df_precaution[self.df_precaution['Disease'] == disease]
        if not prec_row.empty:
            precautions = []
            for col in ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']:
                if col in prec_row.columns:
                    prec = prec_row.iloc[0][col]
                    if pd.notna(prec):
                        precautions.append(prec)
            info['precautions'] = precautions
        
        return info


def main():
    """Main training pipeline"""
    print("=" * 60)
    print("Medical Assistance Chatbot - Model Training")
    print("=" * 60)
    
    # Initialize
    chatbot = MedicalChatbotModel()
    
    # Preprocess data
    X, y = chatbot.preprocess_disease_data()
    
    # Train models
    model = chatbot.train_models()
    
    # Save model
    chatbot.save_model('medical_chatbot_model.pkl')
    
    # Test prediction
    print("\n" + "=" * 60)
    print("Testing Model with Sample Symptoms")
    print("=" * 60)
    
    # Example: Test with symptoms of common cold
    test_symptoms = ['cough', 'high_fever', 'breathlessness']
    test_vector = [0] * len(chatbot.symptom_list)
    
    for symptom in test_symptoms:
        if symptom in chatbot.symptom_list:
            idx = chatbot.symptom_list.index(symptom)
            test_vector[idx] = 1
    
    test_vector = np.array(test_vector).reshape(1, -1)
    prediction = chatbot.disease_model.predict(test_vector)[0]
    probabilities = chatbot.disease_model.predict_proba(test_vector)[0]
    
    print(f"\nTest Symptoms: {test_symptoms}")
    print(f"Predicted Disease: {prediction}")
    
    # Get top 3 predictions
    top_3_idx = np.argsort(probabilities)[-3:][::-1]
    classes = chatbot.disease_model.classes_
    
    print("\nTop 3 Predictions:")
    for idx in top_3_idx:
        print(f"  {classes[idx]}: {probabilities[idx]*100:.2f}%")
    
    # Get disease info
    info = chatbot.get_disease_info(prediction)
    print(f"\nDisease Description: {info['description']}")
    print(f"\nRecommended Precautions:")
    for i, prec in enumerate(info['precautions'], 1):
        print(f"  {i}. {prec}")
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
