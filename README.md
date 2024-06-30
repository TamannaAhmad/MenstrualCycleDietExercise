# MenstrualCycleDietExercise

## Project Problem Statement
To create a website that predicts the user's PCOD risk and calculates their current menstrual phase and expected date of next menses.

Polycystic Ovary Disorder (PCOD) is a common hormonal disorder that affects women of reproductive age. Managing PCOD involves lifestyle changes, including tailored exercise and diet plans. This project aims to provide a comprehensive guide and tool for managing PCOD through personalized exercise and diet plans based on menstrual phases.

The predictions on this project are carried out using data submitted by users through a form on a session basis. The information collected is not stored, ensuring the privacy of data.

## Key Problems
Women with PCOD face numerous challenges, including irregular menstrual cycles, weight gain, and increased risk of diabetes and heart disease. This project addresses the following key problems:
1. Lack of awareness and education about PCOD and its management.
2. Difficulty in accessing personalized exercise and diet plans.
3. Need for a structured approach to manage different menstrual phases.

## Project Goals
1. Educate women about PCOD and its impact on health.
2. Provide personalized exercise and diet plans tailored to each menstrual phase.
3. Offer a user-friendly tool to track menstrual cycles and adjust plans accordingly.

## Project Features
1. **Education Content**: Information on PCOD, menstrual cycle phases, and related terminology.
2. **Data Collection**: A form used to collect data inputs from the user on a sessional basis. 
3. **PCOD Risk Prediction**: Prediction of the user's PCOD risk using a machine learning model trained on a dataset.
4. **Menstrual Cycle Calculation**: Calculation of the user's current menstrual cycle phase and the estimate of the start of their next menses. 
5. **Integrated Chatbot**: An integrated Botpress chatbot that provides diet and exercise recommendations according to the user's menstrual cycle phase.

## Prerequisites:
1. Python 3.x
2. Flask
3. XGBoost
4. Pandas
5. Numpy

## Steps:
1. Clone this repository:
    '''bash
    git clone https://github.com/TamannaAhmad/MenstrualCycleDietExercise
    '''
2. Navigate to the project repository
    '''bash
    cd MenstrualCycleDietExercise
    '''
3. Install the required packages.
    '''bash
    pip install -r requirements.txt
    '''
4. Navigate to the integration directory
    '''bash
    cd integration
    '''
5. Run the Flask application
    '''bash
    python app.py
    '''
6. Open your browser and go to  'http://127.0.0.1:5000'

## Technologies used:
1. Python
2. Flask
3. XGBoost
4. Pandas
5. Numpy
6. HTML/CSS
7. Javascript

## Screenshots
![Website landing page.](/flow well/landing_page1.png)
![Website landing page scrolled down.](/flow well/landing_page2.png)
![Webpage on information about PCOD and menstrual cycle phases.](/flow well/info_page1.png)
![Information page scrolled down.](/flow well/info_page2.png)
![Form where user inputs menstrual cycle data.](/flow well/form_page1.png)
![Form page scrolled down.](/flow well/form_page2.png)
![Result page where the predictions are displayed. Sample output shown.](/flow well/result_page.png)
![Sample of the chatbot integration.](/flow well/result_chatbot.png)


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
