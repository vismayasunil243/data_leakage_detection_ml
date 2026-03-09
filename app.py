from flask import Flask, render_template, request
import joblib
import numpy as np

# Load model and scaler
model = joblib.load("data_leakage_model (2).pkl")
scaler = joblib.load("scaler (2).pkl")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form inputs and convert to integers
        features = [
            int(request.form['Authority']),
            int(request.form['Through_pwd']),
            int(request.form['Through_pin']),
            int(request.form['Through_MFA']),
            int(request.form['Data_Modification']),
            int(request.form['Confidential_Data_Access']),
            int(request.form['Confidential_File_Transfer']),
            int(request.form['External_Destination']),
            int(request.form['File_Operation']),
            int(request.form['Data_Sensitivity_Level'])
        ]

        # Scale and predict
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)

        # Convert prediction to readable output
        result = "⚠️ Data Leakage Detected" if prediction[0] == 1 else "✅ No Data Leakage"

        return render_template("index.html", prediction_text=result)
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)