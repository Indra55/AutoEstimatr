from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
import os
app = Flask(__name__)

model = pickle.load(open(os.path.join(os.path.dirname(__file__), "LinearRegressionModel.pkl"), "rb"))
car = pd.read_csv(os.path.join(os.path.dirname(__file__), "Cleaned_Car_data.csv"))


@app.route('/')
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    years = sorted(car['year'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()
    return render_template('index.html', companies=companies, car_models=car_models, years=years, fuel_type=fuel_type)

@app.route('/predict', methods=['POST'])
def predict():
    company = request.form.get('company')
    car_model = request.form.get('model')   
    year = int(request.form.get('year'))
    fuel_type = request.form.get('fuel_type')
    kms_driven = int(request.form.get('kilometers')) 
    print(company, car_model, year, fuel_type, kms_driven)

    
    prediction = model.predict(pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]], columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']))

    return str(np.round(prediction[0],2))  

if __name__ == "__main__":
    app.run(debug=True)
