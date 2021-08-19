import os
import io
import requests
import ipinfo
from flask import Flask, send_file, request, redirect, url_for, Response

handler = ipinfo.getHandler(os.environ['IPINFO_TOKEN'])


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


def shields_io_url():
    args = {
        # Default badge format
        'label': '{city}',
        'message': '{country_name}',
    } | request.args

    ip = request_ip()
    details = handler.getDetails(ip).details

    params = '&'.join((
        f'{name}={apply_format(value, details)}'
        for name, value in args.items()
    ))

    return f'https://img.shields.io/static/v1?{params}'


def create():
    app = Flask(__name__)

    @app.route('/redirect/badge.svg')
    def badge_redirect():
        # TODO: option to pass default values to formatted variables.
        return redirect(shields_io_url())

    @app.route('/proxy/badge.svg')
    def badge_proxy():
        url = shields_io_url()
        re = requests.get(url=url, data=request.get_data(),
                          cookies=request.cookies)

        data = re.text
        addComment = any(
            # If content type allows for 'html-like' comment
            format in re.headers['content-type']
            for format in ('html', 'svg', 'xml')
        )

        if addComment:
            comment = f'<!-- Badge provided by SHIELDS.IO: {url} -->'
            data = '\n'.join((comment, data))

        headers = {
            name: value
            for name, value in re.headers.items()
            if name.lower() not in {
                'content-encoding', 'content-length',
                'transfer-encoding', 'connection',
            }
        }

        return Response(response=data, headers=headers, status=200)

    return app
