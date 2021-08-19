import io
from flask import Flask, send_file, request, redirect
from img import text_image


def create():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return redirect('/ipinfo.png')

    @app.route('/ipinfo.png')
    def ipinfo():
        arr = io.BytesIO()

        img = text_image('FORWARDED: ' + request.headers['x-forwarded-for'])
        img.save(arr, format='png')

        arr.seek(0)
        return send_file(arr, mimetype='image/png')

    return app
