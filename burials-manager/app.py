from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import requests
import os

app = Flask(__name__)

@app.route('/manager', methods=["GET", "POST"])
def index():
    if request.form:
        try:
            id=request.form.get("delete")
            requests.delete('http://127.0.0.1:6789/site/' + id)
        except Exception as e:
            print("Failed to delete site")
            print(e)
    query = requests.get('http://127.0.0.1:6789/sites')
    sites = None
    sites = []
    for q in query.json():
        sites.append(q)
    return render_template("home.html", sites=sites)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello User!  <a href='/logout'>Logout</a>"
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(port=5002, debug=True)
