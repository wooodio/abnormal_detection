from flask import Flask, render_template, request
from flask_sse import sse
from func.storage_access import parse_url, download_image
import json


app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://localhost'
app.register_blueprint(sse, url_prefix='/event')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/accept', methods=['POST'])
def accept_data():
    msg = json.loads(request.json)

    msg['img_name'] = parse_url(msg['img_url'])[1]

    download_image(msg.pop('img_url'))

    sse.publish(msg, type='abnormal')

    return 'Data received'


if __name__ == '__main__':
    app.run()
