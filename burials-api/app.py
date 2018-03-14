import os

from flask import Flask
from flask import render_template, make_response
from flask import request, Response, jsonify
from flask import redirect
from sqlalchemy import text

from flask_sqlalchemy import SQLAlchemy

import json

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "burials.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

@auth.get_password
def get_password(username):
    if username == 'aaron':
        return 'password'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

class Burials(db.Model):
    id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    state = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    name = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    address = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    longitude = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    latitude = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

@app.route('/', methods=["GET"])
def home():
    return jsonify('Welcome to the burials api')

# gets all sites
@app.route('/sites', methods=['GET'])
def all_sites():
    queries = Burials.query.all()
    sites = []
    for query in queries:
        sites.append([query.id, query.address, query.state, \
                        query.longitude, query.latitude])
    return jsonify(sites)

# gets detail of site
@app.route('/site/<id>', methods=['GET'])
def site_detail(id):
    site = Burials.query.get(id)
    data = json.dumps({'id': site.id, 
                       'name':site.name, 
                       'address':site.address,
                       'state':site.state})
    return data

# deletes site
@app.route('/site/<id>', methods=['DELETE'])
#@auth.login_required
def delete_site(id):
    site = Burials.query.get(id)
    db.session.delete(site)
    db.session.commit()
    return 'site deleted'

# create new site
@app.route("/site", methods=["POST"])
#@auth.login_required
def add_site():
    data = json.loads(request.data)
    site_id = data['id']
    state = data['state']
    name = data['name']
    address = data['address']
    longitude = data['longitude']
    latitude = data['latitude']

    new_site = Burials(id = site_id, 
                       state = state, 
                       name = name, 
                       address = address, 
                       longitude = longitude, 
                       latitude = latitude)

    db.session.add(new_site)
    db.session.commit()

    return jsonify('new site created')

# gets all location lat/longitude
@app.route('/locations', methods=["GET"])
def locations():
    queries = Burials.query.all()
    sites = []
    for query in queries:
        sites.append([query.longitude, query.latitude])

    return json.dumps(sites)

if __name__ == "__main__":
    app.run(debug=True, port=6789)
