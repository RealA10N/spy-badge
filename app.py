import io
from flask import Flask, send_file, request, redirect
from img import generate_image


def create():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return redirect('/ipinfo.png')

    @app.route('/ipinfo.png')
    def ipinfo():

        # Heroku uses an internal routing system to forward the original request,
        # and attaches a 'x-forwarded-for' header to requests.
        # To get the IP address of the original request, we will check the
        # 'x-forwarded-for' header, and will get the last item in the list.

        iplist = request.headers['x-forwarded-for'].split(',')
        ip = iplist[-1]

        img = generate_image(ip)

        arr = io.BytesIO()
        img.save(arr, format='png')

        arr.seek(0)
        return send_file(arr, mimetype='image/png')

    return app
