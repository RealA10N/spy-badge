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
        arr = io.BytesIO()

        img = generate_image(request.remote_addr)
        img.save(arr, format='png')

        arr.seek(0)
        return send_file(arr, mimetype='image/png')

    return app
