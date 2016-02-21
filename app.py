from blinds import Blinds
import time
from flask import Flask, jsonify, make_response, request
from flask.views import View

app = Flask(__name__)

directions = {
    'up': 'trigger_up',
    'down': 'trigger_down',
    'my': 'trigger_my'
}


@app.route('/blinds/channel/<int:channel>/<direction>/', methods=['PUT'])
def blinds_move(channel, direction):
    blinds = app.config['blinds']

    channel -= 1
    if channel < 0 or channel > 4:
        return make_response(jsonify({'status': 'error', 'reason': 'invalid channel'}), 400)

    try:
        trigger = getattr(blinds, directions[direction])
    except KeyError:
        return make_response(jsonify({'status': 'error', 'reason': 'invalid direction'}), 400)

    blinds.set_channel(channel)
    trigger()
    return jsonify({'status': 'ok'})


@app.route('/blinds/channel/<int:channel>/', methods=['POST'])
def blinds_short_move(channel):
    blinds = app.config['blinds']

    channel -= 1
    if channel < 0 or channel > 4:
        return make_response(jsonify({'status': 'error', 'reason': 'invalid channel'}), 400)

    data = request.get_json(force=True)
    try:
        direction = data['direction']
        duration = int(data['duration'])
    except (KeyError, ValueError):
        return make_response(jsonify({
            'status': 'error',
            'reason': 'Invalid payload. Please check payload data'
        }), 400)

    if direction == 'up':
        trigger = blinds.trigger_up
    elif direction == 'down':
        trigger = blinds.trigger_down
    else:
        return make_response(jsonify({'status': 'error', 'reason': 'invalid direction'}), 400)

    if not 0 < duration < 2000:
        return make_response(jsonify({'status': 'error', 'reason': 'duration have to be between 0 and 2000'}), 400)

    blinds.set_channel(channel)
    trigger()
    time.sleep(duration / 1000)
    blinds.trigger_my()

    return jsonify({'status': 'ok'})

@app.route('/blinds/status/', methods=['GET', 'POST'])
def status():
    blinds = app.config['blinds']
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            channel = int(data['channel']) - 1
            if channel < 0 or channel > 4:
                return make_response(jsonify({'status': 'error', 'reason': 'invalid channel'}), 400)
            blinds.set_channel(channel)
        except (KeyError, ValueError):
            return make_response(jsonify({'status': 'error', 'reason': 'invalid payload'}), 400)
    return jsonify({'channel': blinds.channel + 1})

if __name__ == '__main__':
    try:
        blinds = Blinds('/var/run/blinds.channel')
        app.config.update(
            blinds=blinds
        )

        app.run(host='0.0.0.0')
    finally:
        Blinds.cleanup()

