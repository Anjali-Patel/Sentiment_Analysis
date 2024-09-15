import numpy as np
from flask import Flask, request, render_template
import spacy
import logging
import joblib

import warnings

from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
loaded_model = None  # Corrected initialization
nlp = spacy.load("en_core_web_sm")
# Load CountVectorizer
#vectorizer = joblib.load('/Users/anjali/Desktop/Sentiment_analysis/count_vectorizer.joblib')
# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

try:
    # Attempt to load model
    loaded_model = joblib.load('/Users/anjali/Desktop/Sentiment_analysis/naive_bayes_sentiment_model.joblib')

    print("Model loaded successfully.")
except Exception as e:
    # Print error message for model loading failure
    print("Error loading model:", e)
    logging.error("Error loading model: %s", e)

# Check if model is successfully initialized
if loaded_model is None:  # Corrected check
    print("Model not initialized. Please check server logs for details.")
    logging.error("Model not initialized.")

# Load CountVectorizer
vectorizer = CountVectorizer()

@app.route('/')
def home():
    if loaded_model is None:  # Corrected check
        return render_template('home.html', prediction_text="Model not initialized. Please check server logs for details.")
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if loaded_model is None:  # Corrected check
        return render_template('home.html', prediction_text="Model not initialized. Please check server logs for details.")
    
    try:
        # Retrieve form data
        input_comment = request.form['comment']
        
        # Preprocess input comment using spaCy
        doc = nlp(input_comment)
        preprocessed_comment = " ".join([token.lemma_ for token in doc if not token.is_stop])
        
       # Transform preprocessed comment using CountVectorizer
        input_vector = vectorizer.transform([preprocessed_comment])
        
        # Reshape input vector to a 2D array
        input_vector = input_vector.reshape(1, -1)
        
        # Predict sentiment using the loaded model
        prediction = loaded_model.predict(input_vector)
        
        # Convert prediction to text label
        prediction_label = "Positive" if prediction[0] == 0 else "Negative"
        
        return render_template('home.html', prediction_text="Comment Sentiment: {}".format(prediction_label))
    except Exception as e:
        print("An error occurred during prediction:", e)
        logging.error("An error occurred during prediction: %s", e)
        return render_template('home.html', prediction_text="An error occurred during prediction. Please check server logs for details.")

if __name__ == '__main__':
    app.run(debug=True)
