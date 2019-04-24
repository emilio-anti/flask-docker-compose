from flask import Flask, render_template,redirect, url_for, request, jsonify
import redis
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

r = redis.Redis(host='redis', port=6379)

@app.route('/vote', methods=['POST'])
def vote():
	if not r.exists('dogs'):
		r.set('dogs', 0)
	if not r.exists('cats'):
		r.set('cats', 0)
	if request.method == 'POST':
		if 'dogs' in request.form:
			r.incr('dogs')
			response = jsonify({'status': 200})
			return response
		elif 'cats' in request.form:
			r.incr('cats')
			response = jsonify({'status': 200})
			return response

@app.route('/results', methods=['GET'])
def results():
    rp = r.get('dogs')
    rg = r.get('cats')
    result = {'cats' : rg.decode("utf-8") , 'dogs' : rp.decode("utf-8") }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
