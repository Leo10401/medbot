"""
Medical Assistance Chatbot - Interactive Application
This chatbot provides disease predictions, descriptions, precautions, and diet recommendations.
"""

import pickle
import numpy as np
import pandas as pd
import re
from difflib import get_close_matches

class MedicalAssistantChatbot:
    def __init__(self, model_path='medical_chatbot_model.pkl'):
        """Initialize the chatbot with trained model"""
        print("Loading Medical Assistant Chatbot...")
        
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.symptom_list = model_data['symptom_list']
        self.df_severity = model_data['df_severity']
        self.df_description = model_data['df_description']
        self.df_precaution = model_data['df_precaution']
        self.df_diet = model_data['df_diet']
        
        # Create symptom severity dictionary
        self.symptom_severity_dict = dict(zip(
            self.df_severity['Symptom'].str.lower().str.replace('_', ' '),
            self.df_severity['weight']
        ))
        
        print("✓ Chatbot loaded successfully!")
        print(f"✓ Knowledge base: {len(self.symptom_list)} symptoms, {len(self.model.classes_)} diseases")
    
    def normalize_symptom(self, symptom):
        """Normalize symptom name and find closest match"""
        symptom = symptom.lower().strip()
        symptom = re.sub(r'[^\w\s]', '', symptom)
        
        # Try to find exact match first
        symptom_variants = [
            symptom,
            symptom.replace(' ', '_'),
            symptom.replace('_', ' ')
        ]
        
        for variant in symptom_variants:
            if variant in self.symptom_list:
                return variant
        
        # Try fuzzy matching
        matches = get_close_matches(symptom, self.symptom_list, n=1, cutoff=0.7)
        if matches:
            return matches[0]
        
        # Try with underscores
        symptom_underscore = symptom.replace(' ', '_')
        matches = get_close_matches(symptom_underscore, self.symptom_list, n=1, cutoff=0.7)
        if matches:
            return matches[0]
        
        return None
    
    def predict_disease(self, symptoms, top_n=3):
        """Predict disease based on symptoms"""
        # Create symptom vector
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
        
        # Predict
        symptom_vector = np.array(symptom_vector).reshape(1, -1)
        probabilities = self.model.predict_proba(symptom_vector)[0]
        
        # Get top N predictions
        top_indices = np.argsort(probabilities)[-top_n:][::-1]
        predictions = []
        
        for idx in top_indices:
            disease = self.model.classes_[idx]
            confidence = probabilities[idx]
            predictions.append({
                'disease': disease,
                'confidence': confidence * 100
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
            severity = self.symptom_severity_dict.get(symptom_clean, 2)  # Default severity 2
            total_severity += severity
            symptom_severities.append({
                'symptom': symptom,
                'severity': severity
            })
        
        avg_severity = total_severity / len(symptoms) if symptoms else 0
        
        return {
            'total_severity': total_severity,
            'average_severity': avg_severity,
            'symptom_details': symptom_severities,
            'severity_level': self.get_severity_level(avg_severity)
        }
    
    def get_severity_level(self, avg_severity):
        """Classify severity level"""
        if avg_severity >= 4:
            return "CRITICAL - Seek immediate medical attention"
        elif avg_severity >= 3:
            return "HIGH - Consult a doctor soon"
        elif avg_severity >= 2:
            return "MODERATE - Monitor symptoms"
        else:
            return "LOW - Rest and self-care"
    
    def get_diet_recommendation(self, chronic_disease=None, age=None):
        """Get diet recommendations based on health profile"""
        if chronic_disease:
            # Filter by chronic disease
            filtered = self.df_diet[self.df_diet['Chronic_Disease'].str.contains(chronic_disease, case=False, na=False)]
            if not filtered.empty:
                sample = filtered.sample(1).iloc[0]
            else:
                sample = self.df_diet.sample(1).iloc[0]
        elif age:
            # Filter by age range
            age_filtered = self.df_diet[(self.df_diet['Age'] >= age - 10) & (self.df_diet['Age'] <= age + 10)]
            if not age_filtered.empty:
                sample = age_filtered.sample(1).iloc[0]
            else:
                sample = self.df_diet.sample(1).iloc[0]
        else:
            sample = self.df_diet.sample(1).iloc[0]
        
        return {
            'meal_plan': sample['Recommended_Meal_Plan'],
            'calories': sample['Recommended_Calories'],
            'protein': sample['Recommended_Protein'],
            'carbs': sample['Recommended_Carbs'],
            'fats': sample['Recommended_Fats']
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
        
        # Convert to list and limit
        suggested_list = list(suggested)[:max_suggestions]
        
        return suggested_list
    
    def chat(self):
        """Interactive chat interface"""
        print("\n" + "=" * 70)
        print(" " * 15 + "🏥 MEDICAL ASSISTANCE CHATBOT 🏥")
        print("=" * 70)
        print("\nWelcome! I can help you with:")
        print("  • Disease prediction based on symptoms")
        print("  • Disease descriptions and information")
        print("  • Health precautions and recommendations")
        print("  • Diet recommendations")
        print("\nType 'quit' to exit")
        print("=" * 70)
        
        while True:
            print("\n" + "-" * 70)
            user_input = input("\nHow can I assist you today? \n(Describe your symptoms): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Thank you for using Medical Assistant. Stay healthy!")
                break
            
            if not user_input:
                print("⚠️  Please describe your symptoms.")
                continue
            
            # Parse symptoms from input
            symptoms = [s.strip() for s in re.split(r'[,;]', user_input)]
            
            # Iterative symptom collection
            self.analyze_with_iteration(symptoms)
    
    def analyze_with_iteration(self, initial_symptoms):
        """Analyze symptoms iteratively until confidence > 50%"""
        current_symptoms = initial_symptoms.copy()
        
        while True:
            # Predict disease
            predictions, valid_symptoms, invalid_symptoms = self.predict_disease(current_symptoms, top_n=5)
            
            if predictions is None:
                print("\n❌ I couldn't recognize any symptoms from your input.")
                print(f"   Unrecognized: {', '.join(invalid_symptoms)}")
                print("\n💡 Try using medical terms like: fever, cough, headache, fatigue, etc.")
                return
            
            # Display results
            print("\n" + "=" * 70)
            print("📋 ANALYSIS RESULTS")
            print("=" * 70)
            
            # Valid symptoms
            print(f"\n✓ Recognized Symptoms ({len(valid_symptoms)}):")
            for symptom in valid_symptoms:
                print(f"  • {symptom.replace('_', ' ').title()}")
            
            # Invalid symptoms
            if invalid_symptoms:
                print(f"\n⚠️  Unrecognized terms ({len(invalid_symptoms)}):")
                for symptom in invalid_symptoms:
                    print(f"  • {symptom}")
            
            # Severity assessment
            severity_info = self.get_symptom_severity(valid_symptoms)
            print(f"\n🌡️  SEVERITY ASSESSMENT:")
            print(f"   Level: {severity_info['severity_level']}")
            print(f"   Score: {severity_info['total_severity']} (Average: {severity_info['average_severity']:.2f})")
            
            # Check confidence
            max_confidence = predictions[0]['confidence']
            
            # Disease predictions
            print(f"\n🔍 POSSIBLE DIAGNOSES:")
            for i, pred in enumerate(predictions[:3], 1):
                confidence_flag = " [LOW CONFIDENCE]" if pred['confidence'] < 50 else ""
                print(f"\n   {i}. {pred['disease']} (Confidence: {pred['confidence']:.1f}%){confidence_flag}")
                
                # Description
                description = self.get_disease_description(pred['disease'])
                print(f"      📖 {description}")
                
                # Precautions (only for top prediction with good confidence)
                if i == 1 and max_confidence >= 50:
                    precautions = self.get_disease_precautions(pred['disease'])
                    print(f"\n      💊 RECOMMENDED PRECAUTIONS:")
                    for j, prec in enumerate(precautions, 1):
                        print(f"         {j}. {prec.title()}")
            
            # If confidence is low, ask for more symptoms
            if max_confidence < 50:
                print(f"\n" + "=" * 70)
                print(f"⚠️  LOW CONFIDENCE: {max_confidence:.1f}% (Target: >50%)")
                print("=" * 70)
                
                # Get suggested symptoms
                suggested_symptoms = self.get_suggested_symptoms(valid_symptoms, predictions[:3])
                
                if suggested_symptoms:
                    print("\n❓ To improve accuracy, please answer these questions:")
                    print("\nDo you have any of these additional symptoms?")
                    
                    for i, symptom in enumerate(suggested_symptoms, 1):
                        print(f"   {i}. {symptom.replace('_', ' ').title()}")
                    
                    print("\nOptions:")
                    print("  • Enter symptom numbers (e.g., '1,3,5') to add them")
                    print("  • Type 'show' to see diagnosis with current information")
                    print("  • Type 'new' to start over with new symptoms")
                    
                    choice = input("\nYour choice: ").strip().lower()
                    
                    if choice == 'show':
                        # Show final results
                        break
                    elif choice == 'new':
                        return
                    else:
                        # Parse selected symptom numbers
                        try:
                            indices = [int(x.strip()) - 1 for x in choice.split(',')]
                            selected = [suggested_symptoms[i] for i in indices if 0 <= i < len(suggested_symptoms)]
                            
                            if selected:
                                current_symptoms.extend(selected)
                                print(f"\n✓ Added {len(selected)} symptom(s). Re-analyzing...")
                                continue
                            else:
                                print("\n⚠️  No valid symptoms selected. Showing diagnosis with current information.")
                                break
                        except:
                            print("\n⚠️  Invalid input. Showing diagnosis with current information.")
                            break
                else:
                    print("\n💡 No additional symptoms to suggest. Showing diagnosis with current information.")
                    break
            else:
                # Confidence is good, show full results
                break
        
        # Show final results with diet recommendation
        if max_confidence >= 50:
            print(f"\n🍎 DIET RECOMMENDATION:")
            top_disease = predictions[0]['disease']
            chronic_diseases = ['Diabetes', 'Hypertension', 'Heart Disease', 'Obesity']
            chronic_match = next((cd for cd in chronic_diseases if cd.lower() in top_disease.lower()), None)
            
            diet_rec = self.get_diet_recommendation(chronic_disease=chronic_match)
            print(f"   Meal Plan: {diet_rec['meal_plan']}")
            print(f"   Daily Calories: {diet_rec['calories']}")
            print(f"   Protein: {diet_rec['protein']}g | Carbs: {diet_rec['carbs']}g | Fats: {diet_rec['fats']}g")
        
        # Medical disclaimer
        print("\n" + "=" * 70)
        print("⚠️  MEDICAL DISCLAIMER:")
        print("   This is an AI-based prediction system for informational purposes only.")
        print("   Please consult a qualified healthcare professional for proper diagnosis")
        print("   and treatment. In case of emergency, seek immediate medical attention.")
        print("=" * 70)


def main():
    """Main function to run the chatbot"""
    try:
        chatbot = MedicalAssistantChatbot('medical_chatbot_model.pkl')
        chatbot.chat()
    except FileNotFoundError:
        print("❌ Error: Model file not found!")
        print("   Please run 'python train_model.py' first to train the model.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
