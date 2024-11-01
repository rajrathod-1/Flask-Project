from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Password@localhost/covid19'
db = SQLAlchemy(app)

class CovidData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    date = db.Column(db.String(50))
    confirmed = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    recovered = db.Column(db.Integer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data')
def fetch_data():
    url = "https://covid-193.p.rapidapi.com/statistics"
    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY')
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    db.session.query(CovidData).delete()
    db.session.commit()

    for entry in data['response']:
        country = entry['country']
        cases = entry['cases']
        deaths = entry['deaths']
        confirmed = cases['total']
        recovered = cases.get('recovered', 0)
        date = entry['day']

        covid_entry = CovidData(country=country, date=date, confirmed=confirmed, deaths=deaths['total'], recovered=recovered)
        db.session.add(covid_entry)

    db.session.commit()
    return jsonify({"message": "Data fetched and saved successfully!"})

@app.route('/api/data')
def get_data():
    results = CovidData.query.all()
    data = [{"country": r.country, "date": r.date, "confirmed": r.confirmed, "deaths": r.deaths, "recovered": r.recovered} for r in results]
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)
