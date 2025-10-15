"""
Quick test script to verify the iterative symptom collection feature
"""

import pickle
import numpy as np

def test_iterative_feature():
    """Test the iterative symptom collection"""
    
    print("Loading model...")
    with open('medical_chatbot_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    symptom_list = model_data['symptom_list']
    
    print(f"✓ Model loaded: {len(symptom_list)} symptoms, {len(model.classes_)} diseases\n")
    
    # Test Case 1: Few symptoms (should trigger more symptom request)
    print("=" * 60)
    print("TEST CASE 1: Few symptoms (should be < 50% confidence)")
    print("=" * 60)
    test_symptoms = ['cough', 'fever']
    
    symptom_vector = [0] * len(symptom_list)
    for symptom in test_symptoms:
        if symptom in symptom_list:
            idx = symptom_list.index(symptom)
            symptom_vector[idx] = 1
    
    symptom_vector = np.array(symptom_vector).reshape(1, -1)
    probabilities = model.predict_proba(symptom_vector)[0]
    
    top_3_idx = np.argsort(probabilities)[-3:][::-1]
    classes = model.classes_
    
    print(f"\nInput symptoms: {test_symptoms}")
    print(f"\nTop 3 Predictions:")
    for idx in top_3_idx:
        confidence = probabilities[idx] * 100
        flag = " ✓ HIGH" if confidence >= 50 else " ⚠️ LOW"
        print(f"  {classes[idx]}: {confidence:.1f}%{flag}")
    
    max_confidence = probabilities[top_3_idx[0]] * 100
    print(f"\nMax Confidence: {max_confidence:.1f}%")
    print(f"Needs more symptoms: {'YES' if max_confidence < 50 else 'NO'}")
    
    # Test Case 2: More symptoms (should have higher confidence)
    print("\n" + "=" * 60)
    print("TEST CASE 2: More specific symptoms")
    print("=" * 60)
    test_symptoms = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic _patches']
    
    symptom_vector = [0] * len(symptom_list)
    for symptom in test_symptoms:
        # Clean symptom name
        clean_symptom = symptom.strip()
        if clean_symptom in symptom_list:
            idx = symptom_list.index(clean_symptom)
            symptom_vector[idx] = 1
    
    symptom_vector = np.array(symptom_vector).reshape(1, -1)
    probabilities = model.predict_proba(symptom_vector)[0]
    
    top_3_idx = np.argsort(probabilities)[-3:][::-1]
    
    print(f"\nInput symptoms: {test_symptoms}")
    print(f"\nTop 3 Predictions:")
    for idx in top_3_idx:
        confidence = probabilities[idx] * 100
        flag = " ✓ HIGH" if confidence >= 50 else " ⚠️ LOW"
        print(f"  {classes[idx]}: {confidence:.1f}%{flag}")
    
    max_confidence = probabilities[top_3_idx[0]] * 100
    print(f"\nMax Confidence: {max_confidence:.1f}%")
    print(f"Needs more symptoms: {'YES' if max_confidence < 50 else 'NO'}")
    
    print("\n" + "=" * 60)
    print("✓ Testing complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_iterative_feature()
    except FileNotFoundError:
        print("❌ Error: Model file not found!")
        print("   Please run 'python train_model.py' first to train the model.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
