from flask import make_response, jsonify
from api_v1 import app

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not  Found'}), 404)


@app.errorhandler(400)
def bad_requsest(error):
    return make_response(jsonify({'error': 'Bad Requesst'}), 400)