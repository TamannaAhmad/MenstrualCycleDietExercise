from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    cycle_day = None
    if request.method == 'POST':
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        cycle_length = int(request.form['cycleLength'])
        menses_length = int(request.form['mensesLength'])
        unusual_bleeding = request.form.get('unusualBleeding') == 'on'
        last_period_start = request.form['lastPeriodStart']

        last_period_date = datetime.strptime(last_period_start, '%Y-%m-%d')
        current_date = datetime.now()
        day_diff = (current_date - last_period_date).days
        cycle_day = day_diff % cycle_length

    return render_template('index.html', cycle_day=cycle_day)

if __name__ == '__main__':
    app.run(debug=True)