#!flask/bin/python
import six
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import json

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


with open("obesity_census_data.json") as read_file:
    obesity_census_data = json.load(read_file)

with open("playtime_data.json") as read_file:
    playtime_data = json.load(read_file)

with open("obesity_polygon_data.json") as read_file:
    obesity_polygon_data = json.load(read_file)

with open("mental_census_data.json") as read_file:
    mental_census_data = json.load(read_file)

with open("mental_polygon_data.json") as read_file:
    mental_polygon_data = json.load(read_file)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'],
                                      _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/todo/api/v1.0/obesity_census_data', methods=['GET'])
@auth.login_required
def get_obesity_census_data():
    return jsonify(obesity_census_data)

@app.route('/todo/api/v1.0/playtime_data', methods=['GET'])
@auth.login_required
def get_playtime_data():
    return jsonify(playtime_data)

@app.route('/todo/api/v1.0/obesity_polygon_data', methods=['GET'])
@auth.login_required
def get_obesity_polygon_data():
    return jsonify(obesity_polygon_data)

@app.route('/todo/api/v1.0/mental_census_data', methods=['GET'])
@auth.login_required
def get_mental_census_data():
    return jsonify(mental_census_data)

@app.route('/todo/api/v1.0/mental_polygon_data', methods=['GET'])
@auth.login_required
def get_mental_polygon_data():
    return jsonify(mental_polygon_data)

if __name__ == '__main__':
    app.run(debug=True)
