from app import app
from flask import make_response, jsonify
import requests


my_api_key = 'c34143464249e4b2c000f1a05e5172c7'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return None


def get_city(city):
    city_list=[]


@app.route('/', methods=['GET'])
def current_day():
    city = 'Montego Bay'
    api_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, my_api_key)
    response = requests.get(api_url).json()

    return response


@app.route('/five_day_forecast', methods=['GET'])
def five_day():
    city = 'Kingston'
    api_url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'.format(city, my_api_key)
    response = requests.get(api_url).json()

    return response


one_day_forecast = current_day()
five_day_forecast = five_day()


@app.route('/temp/<int:day>', methods=['GET'])
def get_temp(day):

    result = dict()

    if day == 1:
        current_temp = one_day_forecast["main"]
        convert_current_temp = int(current_temp["temp"] - 273.15)
        result["current temperature"] = convert_current_temp
    elif day == 5:
        result["temperature list"] = []
        for day in five_day_forecast["list"]:
            current_days_temp = dict()
            current_days_temp["current temperature"] = int(day["main"]["temp"] - 273.15)
            result["temperature list"].append(current_days_temp)
    return jsonify(result)


@app.route('/wind/<int:day>', methods=['GET'])
def get_wind_speed(day):
    result = dict()

    if day == 1:
        current_wind = one_day_forecast["wind"]
        convert_current_wind = int(current_wind["speed"] * 2.24)
        result["Current Wind Speeds"] = convert_current_wind
    elif day == 5:
        result["wind speed list"] = []
        for days in five_day_forecast["list"]:
            wind_speed = dict()
            wind_speed["Day's wind speed"] = int(days["wind"]["speed"] * 2.24)
            result["wind speed list"].append(wind_speed)
    return jsonify(result)


@app.route('/cloud/<int:day>', methods=['GET'])
def get_cloud_forecast(day):
    result = dict()

    if day == 1:
        current_cloud = one_day_forecast["clouds"]["all"]
        result["Current Cloud Forecast"] = current_cloud
    elif day == 5:
        result["Current Cloud Forecast list"] = []

        for days in five_day_forecast["list"]:
            cloud_forecast = dict()
            cloud_forecast["Day's Current Cloud Forecast"] = days["clouds"]["all"]
            result["Current Cloud Forecast list"].append(cloud_forecast)
    return jsonify(result)


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
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
