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
        number_of_peak = int(data['number_of_peak'])  

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
        return np.array([processed_data]), last_menses_start_date, last_menses_end_date, estimated_ovulation, avg_cycle_length, avg_menses_length
    except KeyError as e:
        raise ValueError(f"Missing key in form data: {e}")

#function to predict the cycle phase of user
def predict_cycle_phase(last_menses_start_date, last_menses_end_date, estimated_ovulation, avg_cycle_length, avg_menses_length):  
    today = pd.Timestamp.today()
    cycle_day = (today-last_menses_start_date).days #calculate the cycle day in relation to current day
    ovulation_day = (estimated_ovulation - last_menses_start_date).days
    #if available use last_menses_end_date for accuracy:
    if pd.notnull(last_menses_end_date):
        menses_duration = (last_menses_end_date - last_menses_start_date).days + 1
    else:
        menses_duration = avg_menses_length

    if cycle_day <= menses_duration:
        return "Menstrual Phase", cycle_day
    elif menses_duration < cycle_day <= ovulation_day:
        return "Follicular Phase", cycle_day
    elif cycle_day == ovulation_day:
        return "Approximate Day of Ovulation", cycle_day
    elif ovulation_day < cycle_day <= avg_cycle_length:
        return "Luteal Phase", cycle_day
    else:
        return "Irregular Cycle", cycle_day

#function to calculate next menses date
def next_menses_date(last_menses_start_date, avg_cycle_length):
    next_start_date = last_menses_start_date + pd.Timedelta(days=(avg_cycle_length))
    return next_start_date

#define routes for webpage links
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
            input_data, last_menses_start_date, last_menses_end_date, estimated_ovulation, avg_cycle_length, avg_menses_length = prepare_input(form_data)
            prediction = model.predict(input_data)

            if prediction < 3:
                pcod_risk = "Low risk of PCOD"
            elif prediction == 3:
                pcod_risk = "Moderate risk of PCOD"
            else:
                pcod_risk = "High risk of PCOD"
            
            cycle_phase, cycle_day = predict_cycle_phase(last_menses_start_date, last_menses_end_date, estimated_ovulation, avg_cycle_length, avg_menses_length)
            next_menses_start_date = next_menses_date(last_menses_start_date, avg_cycle_length)
            return render_template('result.html', pcod_risk=pcod_risk, cycle_phase=cycle_phase, cycle_day=cycle_day, next_menses=next_menses_start_date.strftime('%d-%m-%Y'))
        except ValueError as e:
            return str(e), 400   # Return error message and 400 status code for bad request

if __name__ == '__main__':
    app.run(debug=True)