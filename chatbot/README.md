# 🏥 Medical Assistance Chatbot

An AI-powered medical assistance chatbot that predicts diseases based on symptoms and provides comprehensive health guidance including disease descriptions, precautions, severity assessment, and personalized diet recommendations.

## 📋 Features

- **Disease Prediction**: Predicts potential diseases based on input symptoms using machine learning
- **Iterative Symptom Collection**: 🆕 Intelligently asks for more symptoms until confidence reaches >50%
- **Smart Symptom Suggestions**: 🆕 Suggests relevant symptoms based on possible diagnoses
- **Interactive Symptoms Sidebar**: 🆕 Browse and click from 130+ available symptoms
- **Real-time Search**: 🆕 Filter symptoms instantly with search functionality
- **Symptom Analysis**: Recognizes and normalizes medical symptoms with fuzzy matching
- **Severity Assessment**: Calculates severity scores for symptoms to determine urgency
- **Confidence Scoring**: Shows confidence levels for each prediction with visual indicators
- **Disease Information**: Provides detailed descriptions for predicted diseases
- **Health Precautions**: Offers actionable precautions and recommendations
- **Diet Recommendations**: Suggests personalized diet plans based on health conditions
- **Multiple Interfaces**: 
  - Command-line interface (CLI)
  - Web API (Flask REST API)
  - Web UI (HTML/CSS/JavaScript)

## 📊 Datasets

The system uses 5 comprehensive medical datasets:

1. **dataset.csv**: Disease-symptom mappings (4,920+ records)
2. **Symptom-severity.csv**: Symptom severity weights
3. **symptom_Description.csv**: Disease descriptions
4. **symptom_precaution.csv**: Disease precautions and recommendations
5. **Personalized_Diet_Recommendations.csv**: Diet recommendations based on health profiles

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or navigate to the project directory**:
```bash
cd c:\Users\kanha\OneDrive\Desktop\medaii\chatbot
```

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

## 📦 Usage

### Step 1: Train the Model

First, train the machine learning model using the datasets:

```bash
python train_model.py
```

This will:
- Load and preprocess all datasets
- Extract and normalize symptoms
- Train multiple ML models (Random Forest, Gradient Boosting, SVM)
- Select the best performing model
- Save the trained model as `medical_chatbot_model.pkl`

Expected output:
```
Loading datasets...
✓ Loaded 4920 disease records
✓ Found 132 unique symptoms
✓ Created feature matrix
✓ Training models...
✓ Best model: Random Forest with accuracy 0.95+
✓ Model saved successfully!
```

### Step 2: Use the Chatbot

#### Option A: Command-Line Interface

Run the interactive CLI chatbot:

```bash
python chatbot.py
```

Example interaction:
```
🏥 MEDICAL ASSISTANCE CHATBOT 🏥

How can I assist you today?
(Describe your symptoms): fever, cough, fatigue, headache

📋 ANALYSIS RESULTS
✓ Recognized Symptoms (4):
  • Fever
  • Cough
  • Fatigue
  • Headache

🌡️ SEVERITY ASSESSMENT:
   Level: MODERATE - Monitor symptoms
   Score: 8 (Average: 2.00)

🔍 POSSIBLE DIAGNOSES:
   1. Common Cold (Confidence: 87.3%)
      📖 The common cold is a viral infection...
      
      💊 RECOMMENDED PRECAUTIONS:
         1. Drink vitamin c rich drinks
         2. Take vapour
         3. Avoid cold food
         4. Keep fever in check
```

#### Option B: Web API

1. **Start the Flask API server**:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

2. **API Endpoints**:

- `GET /` - API information
- `GET /health` - Health check
- `GET /symptoms` - List all available symptoms
- `GET /diseases` - List all diseases
- `POST /predict` - Predict disease from symptoms
- `GET /disease-info/<name>` - Get disease information

3. **Example API Request**:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d "{\"symptoms\": [\"fever\", \"cough\", \"headache\"]}"
```

#### Option C: Web Interface

1. **Start the Flask API server** (if not already running):
```bash
python app.py
```

2. **Open the web interface**:
   - Open `index.html` in your web browser
   - Or navigate to the file location and double-click it

3. **Use the interface**:
   - Enter symptoms in the text area (comma-separated)
   - Click "🔍 Analyze Symptoms"
   - View comprehensive results including:
     - Recognized symptoms
     - Severity assessment
     - Disease predictions with confidence scores
     - Precautions
     - Diet recommendations

## 🧠 Machine Learning Models

The system trains and compares three models:

1. **Random Forest Classifier**
   - Ensemble method with 100 decision trees
   - Best for handling multiple symptom combinations
   - Typically achieves 95%+ accuracy

2. **Gradient Boosting Classifier**
   - Sequential ensemble learning
   - Good for complex patterns
   - Typically achieves 93%+ accuracy

3. **Support Vector Machine (SVM)**
   - RBF kernel for non-linear classification
   - Good for high-dimensional data
   - Typically achieves 90%+ accuracy

The best performing model is automatically selected and saved.

## 📁 Project Structure

```
chatbot/
├── dataset/
│   ├── dataset.csv                          # Disease-symptom mappings
│   ├── Symptom-severity.csv                 # Symptom severity weights
│   ├── symptom_Description.csv              # Disease descriptions
│   ├── symptom_precaution.csv               # Disease precautions
│   └── Personalized_Diet_Recommendations.csv # Diet recommendations
├── train_model.py                            # Model training script
├── chatbot.py                                # CLI chatbot interface
├── app.py                                    # Flask web API
├── index.html                                # Web UI
├── requirements.txt                          # Python dependencies
├── medical_chatbot_model.pkl                 # Trained model (generated)
└── README.md                                 # This file
```

## 🔬 Technical Details

### Symptom Processing
- **Normalization**: Converts symptoms to standardized format
- **Fuzzy Matching**: Uses Levenshtein distance to match similar symptom names
- **Binary Encoding**: Creates feature vectors for ML model input

### Disease Prediction
- **Multi-label Classification**: Predicts multiple possible diseases
- **Confidence Scores**: Provides probability for each prediction
- **Top-N Results**: Returns top 3 most likely diseases

### Severity Calculation
- **Weighted Scores**: Each symptom has a severity weight (1-5)
- **Classification Levels**:
  - LOW (0-2): Rest and self-care
  - MODERATE (2-3): Monitor symptoms
  - HIGH (3-4): Consult doctor soon
  - CRITICAL (4+): Seek immediate medical attention

## ⚠️ Medical Disclaimer

**IMPORTANT**: This is an AI-based prediction system for informational and educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

- Always consult a qualified healthcare professional for medical concerns
- In case of emergency, seek immediate medical attention
- Do not use this system for self-diagnosis or self-medication
- The predictions are based on limited data and may not be accurate

## 🛠️ Troubleshooting

### Issue: Model file not found
**Solution**: Run `python train_model.py` first to train and save the model.

### Issue: Import errors
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Issue: Web interface can't connect to API
**Solution**: 
1. Make sure Flask server is running (`python app.py`)
2. Check that the API is accessible at `http://localhost:5000`
3. Check for CORS issues in browser console

### Issue: Poor prediction accuracy
**Solution**: 
1. Use medical terminology for symptoms
2. Provide multiple symptoms (3-5 recommended)
3. Check spelling and symptom names

## 🔄 Model Retraining

To retrain the model with updated datasets:

1. Update the CSV files in the `dataset/` folder
2. Run: `python train_model.py`
3. The new model will overwrite `medical_chatbot_model.pkl`

## 📈 Performance Metrics

Expected model performance:
- **Accuracy**: 95%+
- **Precision**: 93%+
- **Recall**: 92%+
- **F1-Score**: 93%+

## 🤝 Contributing

To improve the chatbot:
1. Add more disease-symptom mappings to datasets
2. Enhance symptom normalization algorithms
3. Integrate additional medical knowledge bases
4. Improve UI/UX design

## 📝 License

This project is for educational purposes. Medical datasets are from public sources.

## 👨‍💻 Support

For issues or questions:
1. Check this README
2. Review the code comments
3. Test with example symptoms first

## � Iterative Symptom Collection

The chatbot now features **intelligent symptom collection** that ensures accurate diagnoses:

### How It Works:
1. **Initial Analysis**: User enters their symptoms
2. **Confidence Check**: System checks if prediction confidence is >50%
3. **Smart Suggestions**: If confidence is low, system suggests relevant additional symptoms
4. **User Selection**: User selects applicable symptoms from suggestions
5. **Re-Analysis**: System re-analyzes with expanded symptom set
6. **Repeat**: Process continues until confidence >50% or user chooses to proceed

### Example Flow:

```
User enters: "fever, cough"
→ Confidence: 35% (LOW)
→ System suggests: headache, fatigue, body ache, sore throat, etc.
→ User selects: headache, fatigue
→ Re-analysis with: fever, cough, headache, fatigue
→ Confidence: 68% (HIGH) ✓
→ Shows detailed diagnosis and recommendations
```

### Benefits:
- ✅ More accurate diagnoses
- ✅ Guided symptom discovery
- ✅ Prevents premature conclusions
- ✅ User remains in control (can skip if needed)

## �🎯 Future Enhancements

- [x] Iterative symptom collection with confidence thresholds
- [x] Smart symptom suggestions based on possible diseases
- [ ] Add multi-language support
- [ ] Integrate with medical APIs
- [ ] Add symptom duration tracking
- [ ] Implement user history
- [ ] Add medication suggestions
- [ ] Mobile app development
- [ ] Voice input support
- [ ] Integration with wearable devices

---

**Version**: 1.0  
**Last Updated**: October 2025  
**Python Version**: 3.8+

---

## Quick Start Guide

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the model
python train_model.py

# 3. Run the chatbot (choose one):

# CLI version:
python chatbot.py

# Web API + UI version:
python app.py
# Then open index.html in browser
```

Enjoy using the Medical Assistance Chatbot! 🏥💙
