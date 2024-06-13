from flask import Flask, request, render_template_string, render_template
import xgboost as xgb
import numpy as np
import pandas as pd
import os

# Define the paths for the template and static folders
template_dir = os.path.abspath('../frontend')
static_dir = os.path.abspath('../frontend')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Load the model
model = xgb.XGBClassifier()
model.load_model('../model.bin')

# Function to prepare the input data
def prepare_input(data):
    try:
        age = int(data['age'])
        height = float(data['height']) / 100  # Convert height from cm to meters
        weight = float(data['weight'])
        avg_cycle_length = int(data['avg_cycle_length'])
        avg_menses_length = int(data['avg_menses_length'])
        number_of_peak = int(data['number_of_peak'])  # Ensure correct key usage

        # Convert unusual_bleeding to 1 or 0
        unusual_bleeding = 1 if data['unusual_bleeding'] == 'yes' else 0

        # Convert date strings to datetime objects and calculate relevant values
        last_menses_start_date = pd.to_datetime(data['last_menses_start_date'])
        last_menses_end_date = pd.to_datetime(data['last_menses_end_date'])
        estimated_ovulation = last_menses_start_date + pd.Timedelta(days=avg_cycle_length // 2)
        luteal_phase_length = avg_cycle_length - (avg_cycle_length // 2)

        # Calculate BMI
        bmi = weight / (height * height)

        # Calculate Mean Length of Cycle
        mean_cycle_length = (avg_cycle_length + avg_menses_length) / 2

        processed_data = [
            number_of_peak, age, avg_cycle_length, avg_cycle_length//2, luteal_phase_length,
            avg_menses_length, unusual_bleeding, weight, bmi, mean_cycle_length
        ]
        return np.array([processed_data]), last_menses_start_date, estimated_ovulation, avg_cycle_length, avg_menses_length, luteal_phase_length
    except KeyError as e:
        raise ValueError(f"Missing key in form data: {e}")

def predict_cycle_phase(last_menses_start_date, estimated_ovulation, avg_cycle_length, avg_menses_length, luteal_phase_length):  
    today = pd.Timestamp.today()
    cycle_day = (today-last_menses_start_date).days 
    ovulation_day = (estimated_ovulation - last_menses_start_date).days
    luteal_phase_start = ovulation_day + 1
    if cycle_day <= avg_menses_length:
        return "Menstrual Phase"
    elif avg_menses_length < cycle_day <= ovulation_day:
        return "Follicular Phase"
    elif cycle_day == ovulation_day:
        return "Approximate Day of Ovulation"
    elif ovulation_day < cycle_day <= avg_cycle_length:
        return "Luteal Phase"
    else:
        return "Irregular Cycle"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/form')
def get_plan():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            form_data = request.form
            input_data, last_menses_start_date, estimated_ovulation, avg_cycle_length, avg_menses_length, luteal_phase_length = prepare_input(form_data)
            prediction = model.predict(input_data)

            if prediction < 3:
                pcod_risk = "Low risk of PCOD"
            elif prediction == 3:
                pcod_risk = "Moderate risk of PCOD"
            else:
                pcod_risk = "High risk of PCOD"
            
            cycle_phase = predict_cycle_phase(last_menses_start_date, estimated_ovulation, avg_cycle_length, avg_menses_length, luteal_phase_length)

            return render_template('result.html', pcod_risk=pcod_risk, cycle_phase=cycle_phase)
        except ValueError as e:
            return str(e), 400   # Return error message and 400 status code for bad request

if __name__ == '__main__':
    app.run(debug=True)