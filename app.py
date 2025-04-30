# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
import requests
from config import MONGO_URI, SECRET_KEY, OPENAI_API_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

client = MongoClient(MONGO_URI)
db = client.get_database()
users_collection = db.users

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    user_doc = users_collection.find_one({"user_id": user_id})
    return User(user_id) if user_doc else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({"username": username})
        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User(user['user_id'])
            login_user(user_obj)
            return redirect(url_for('get_quote'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/get-quote', methods=['GET', 'POST'])
@login_required
def get_quote():
    if request.method == 'POST':
        historical_figure = request.form['historical_figure']
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            "prompt": f"Quote by {historical_figure}:",
            "max_tokens": 50
        }
        response = "Random text, but not working ... as shoudl jet."
        if response is not None:
            quote = response
            return jsonify({"quote": quote})
        else:
            return jsonify({"error": "Failed to fetch quote"}), 500
    return '''
    <form method="POST">
        Historical Figure Name: <input type="text" name="historical_figure">
        <input type="submit" value="Get Quote">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
