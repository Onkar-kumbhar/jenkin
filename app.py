from flask import Flask, request, render_template_string, render_template, redirect
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # A2: Hardcoded secret

@app.route('/')
def home():
    return "Welcome to the vulnerable app!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        # A1: SQL Injection (unsafe input directly in query)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username='{user}' AND password='{pwd}'")
        result = cursor.fetchone()
        conn.close()

        if result:
            return f"Welcome, {user}!"
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/eval')
def unsafe_eval():
    code = request.args.get('code')
    return str(eval(code))  # A1: Arbitrary code execution

@app.route('/ssrf')
def ssrf():
    import requests
    url = request.args.get('url')
    return requests.get(url).text  # A10: SSRF vulnerability

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5050)

