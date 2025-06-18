import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # For session management

# Load the model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Redirect root to login page
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123prediction':
            session['user'] = username
            return redirect(url_for('predict'))
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)

# Prediction route (also shows the form)
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        features = [float(x) for x in request.form.values()]
        final_features = scaler.transform([np.array(features)])
        prediction = model.predict(final_features)
        output = round(prediction[0], 2)

        if output == 0:
            session['result'] = 'THE PATIENT IS NOT LIKELY TO HAVE A HEART FAILURE'
        else:
            session['result'] = 'THE PATIENT IS LIKELY TO HAVE A HEART FAILURE'

        return redirect(url_for('result'))

    return render_template('index.html')

# For API access
@app.route('/result')
def result():
    if 'user' not in session:
        return redirect(url_for('login'))

    result = session.get('result', 'No prediction made.')
    return render_template('result.html', result=result)


if __name__ == "__main__":
    app.run(debug=False)
