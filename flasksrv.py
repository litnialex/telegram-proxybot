#!/usr/bin/env python3
import os
import asyncio
from flask import Flask, request
from proxybot.bot import telegramma

FLASK_APP_PORT = os.environ.get('FLASK_APP_PORT', 8080)
FLASK_SSL_PORT = os.environ.get('FLASK_SSL_PORT', 8443)
FLASK_SSL_CERT = os.environ.get('FLASK_SSL_CERT', 'ssl/cert.pem')
FLASK_SSL_KEY = os.environ.get('FLASK_SSL_KEY', 'ssl/privkey.pem')
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)

# Enable SSL if certificate and key available
app_dir = os.path.dirname(os.path.abspath(__file__))
ssl_cert = os.path.join(app_dir, FLASK_SSL_CERT)
ssl_key = os.path.join(app_dir, FLASK_SSL_KEY)
try:
    os.stat(ssl_cert) and os.stat(ssl_key)
    kwargs = {'port': FLASK_SSL_PORT, 'ssl_context': (ssl_cert, ssl_key)}
except FileNotFoundError:
    kwargs = {'port': FLASK_APP_PORT}

app = Flask(__name__)

# TOKEN is expected as path or as param "token"
@app.route('/', defaults={'token': ''}, methods=["POST"])
@app.route('/<string:token>', methods=["POST"])
def proxybot_route(token):
    return asyncio.run(telegramma(request))


if __name__ == '__main__':
    app.run(debug=bool(FLASK_DEBUG), host='0.0.0.0', **kwargs)
