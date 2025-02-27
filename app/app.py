from flask import Flask, jsonify
import os
import socket
import datetime

# Initialize Flask application
app = Flask(__name__)

# Configuration from environment variables (default values provided)
APP_NAME = os.environ.get('APP_NAME', 'K8s Test App')
APP_VERSION = os.environ.get('APP_VERSION', '1.0')

# Track request count to demonstrate statelessness in Kubernetes
request_count = 0

@app.route('/')
def index():
    """Main page showing container/pod information"""
    global request_count
    request_count += 1
    
    # Return proper HTML structure
    return """<!DOCTYPE html>
    <html>
    <head>
        <title>Kubernetes Mini Demo</title>
    </head>
    <body>
        <h1>Kubernetes Mini Demo</h1>
        <p>App: {} v{}</p>
        <p>Hostname (Pod name): {}</p>
        <p>Pod IP: {}</p>
        <p>Request count: {}</p>
        <p>Time: {}</p>

        <p><a href="/api/info"><button>View API Info</button></a></p>
        <p><a href="/api/health"><button>Health Check</button></a></p>
    </body>
    </html>
    """.format(APP_NAME, APP_VERSION, socket.gethostname(), socket.gethostbyname(socket.gethostname()), request_count, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/details')
def details():
    """Returns application details as JSON."""
    return jsonify({
        'application': APP_NAME,
        'version': APP_VERSION,
        'hostname': socket.gethostname(),
        'pod_ip': socket.gethostbyname(socket.gethostname()),
        'request_count': request_count
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'server': socket.gethostname()
    })

@app.route('/api/time')
def server_time():
    """Returns the server's current date and time."""
    return jsonify({
        'current_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'timezone': 'UTC'
    })

if __name__ == '__main__':
    # Read port from environment variables (default to 5000)
    port = int(os.environ.get('PORT', 5000))
    print(f"🔥 Starting {APP_NAME} v{APP_VERSION} on port {port}")
    app.run(host='0.0.0.0', port=port)
