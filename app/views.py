from app import app
from flask import render_template, request, make_response, jsonify
import requests
import json


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return None


@app.route('/', methods=['GET'])
def current_day():
    my_api_key = 'c34143464249e4b2c000f1a05e5172c7'
    city = 'Montego Bay'

    apikey_ = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, my_api_key)
    response = requests.get(apikey_)

    return response.json()


@app.route('/five_day_forecast', methods=['GET'])
def five_day():
    myapikey = 'c34143464249e4b2c000f1a05e5172c7'
    citi = 'Kingston'

    apikey_ = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'.format(citi, myapikey)
    responser = requests.get(apikey_)

    return responser.json()


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)
    return error_messages


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return make_response(jsonify({ 'error' : 'Not Found' }), 404)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
