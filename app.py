
import requests
import json

from flask import Flask, request, jsonify


app = Flask(__name__)

def get_ip_info(ip_address):
    r = requests.get(f'http://ipwhois.app/json/{ip_address}')
    return r.json()

def get_html(ip_info):
    city = ip_info['city']
    isp = ip_info['isp']
    lat = ip_info['latitude']
    lng = ip_info['longitude']

    html = f"""
    <h1>Welcome to the party!</h1>
    So I have some info you might find interesting...
    <br/>
    Someone told me they saw you near { city }
    <br/>
    Are you happening to use { isp } for your internet?
    <br/>
    <a href="https://www.openstreetmap.org/#map=18/{ lat }/{ lng }">https://www.openstreetmap.org/#map=18/{ lat }/{ lng }</a>
    """

    return html

@app.route('/', methods=['GET'])
def index():
    ip = request.headers.get('X-Forwarded-For')
    if not ip:
        ip = request.remote_addr

    ip_info = get_ip_info(ip)

    print(json.dumps(ip_info, indent=2))

    html = get_html(ip_info)

    return html, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
