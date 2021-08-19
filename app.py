import os
import io

import ipinfo
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, send_file, request, redirect, url_for

handler = ipinfo.getHandler(os.environ['IPINFO_TOKEN'])
font = ImageFont.load_default()


def text_image(text: str):
    size = font.getsize(text)
    img = Image.new('L', size, color='black')

    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, fill='white', font=font)

    return img


def create():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return redirect(url_for('badge', **request.args))

    @app.route('/badge.png')
    def badge():

        # Heroku uses an internal routing system to forward the original request,
        # and attaches a 'x-forwarded-for' header to requests.
        # To get the IP address of the original request, we will check the
        # 'x-forwarded-for' header, and will get the last item in the list.
        ip = request.headers['x-forwarded-for'].split(',')[-1]
        details = handler.getDetails(ip).details

        # Default badge text will just show the ip of the user request.
        # If format is provided using the 'format' param, will use that!
        text = request.args.get('format') or '{ip}'

        # Replace variables in format with actual data
        for old, new in details.items():
            print(f'{old=}, {new=}')
            text = text.replace(f'{{{old}}}', new)

        # Generate image from given text
        img = text_image(text)

        # Save image to memory
        arr = io.BytesIO()
        img.save(arr, format='png')

        # Return the image as a file
        arr.seek(0)
        return send_file(arr, mimetype='image/png')

    return app
