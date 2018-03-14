from flask import Flask, render_template, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import requests, json

app = Flask(__name__)

#app.config['GOOGLEMAPS_KEY'] = ""

GoogleMaps(app)

@app.route('/')
def hello():
    return jsonify({'message': 'Hello, Burials Map!'})

@app.route('/map/')
def map_unbounded():
    """Create map with markers out of bounds."""
    r = requests.get('http://127.0.0.1:6789/locations')
    global locations
    locations = r.json()    # long list of coordinates
    mymap = Map(
        identifier="burialssmap",
        lat=locations[0][1],
        lng=locations[0][0],
        markers=[(float(loc[1]), float(loc[0])) for loc in locations],
        fit_markers_to_bounds = True,
    )
    return render_template('burials.html', mymap=mymap)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
