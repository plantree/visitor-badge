from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)

counter_service = 'http://api.counter.plantree.me'
# counter_service = 'http://localhost:3000'

@app.route('/')
def home():
    return redirect('https://plantree.github.io/project-docs/', code=302)

@app.route('/visitor-badge/pv')
def visitor_badge_pv():
    args = request.args
    # check args
    if 'namespace' not in args or 'key' not in args:
        return jsonify({'error': 'need namespace and key '}), 400
    namespace = args['namespace']
    key = args['key']
    url = f'{counter_service}/pv/increment?namespace={namespace}&key={key}'
    res = requests.post(url, verify=False)
    if res.status_code != 200:
        return jsonify(res.json()), res.status_code
    
    message = res.json()['data'][0]['value']
    label = 'pv'
    if 'label' in args:
        label = args['label']
    labelColor = 'grey'
    if 'labelColor' in args:
        labelColor = args['labelColor']
    color = 'green'
    if 'color' in args:
        color = args['color']
    style = 'flat'
    if 'style' in args:
        style = args['style']
    return redirect(f'https://img.shields.io/badge/{label}-{message}-{color}?labelColor={labelColor}&style={style}', code=302)


if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
