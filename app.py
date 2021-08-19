import os
import io

import ipinfo
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, send_file, request, redirect, url_for

handler = ipinfo.getHandler(os.environ['IPINFO_TOKEN'])
font = ImageFont.load_default()


def apply_format(text: str, details: dict):
    for old, new in details.items():
        text = text.replace(f'{{{old}}}', str(new))
    return text


def request_ip() -> str:

    # If request is forwarded by some server, the forwarded request
    # should have a header that is attached by the forwarding server
    # with the name 'x-forwarded-for'.
    header = request.headers.get('x-forwarded-for')

    if header:
        # The header stores a list of ips in a stack, where the last one
        # in the list is the original ip of the original request. List
        # values are seperated by ','.
        return header.split(',')[-1]

    else:
        # If request is not forwarded, return basic request ip.
        return request.remote_addr

    return request.headers['x-forwarded-for'].split(',')[-1]


def create():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return redirect(url_for('badge_svg', **request.args))

    @app.route('/badge.svg')
    def badge_svg():

        label = request.args.get('label') or '{city}'
        message = request.args.get('message') or '{country_name}'
        color = request.args.get('color')

        ip = request_ip()
        details = handler.getDetails(ip).details

        params = '&'.join((
            f'{name}={apply_format(value, details)}'
            for name, value in {
                'label': label,
                'message': message,
                'color': color,
            }.items()
            if value is not None
        ))

        return redirect(f'https://img.shields.io/static/v1?{params}')

    return app
