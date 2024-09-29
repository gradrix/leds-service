from flask import Flask, send_from_directory
from api.endpoints import register_api

app = Flask(__name__)

register_api(app)

@app.route('/')
def index():
    return send_from_directory('frontend_build', 'index.html')

@app.route('/content/favicon.ico')
def favicon():
    return send_from_directory('frontend_build', 'favicon.ico')

@app.route('/content/js/<path:path>')
def serve_js(path):
    return send_from_directory('frontend_build/js', path)

@app.route('/content/css/<path:path>')
def serve_css(path):
    return send_from_directory('frontend_build/css', path)

@app.route('/content/<path:path>')
def serve_static(path):
    # Handle any additional static files here, if needed
    return send_from_directory('frontend_build', path)

if __name__ == '__main__':
    app.run(debug=True)