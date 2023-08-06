from flask import Flask, Response, render_template
from flask_basicauth import BasicAuth
from .camera import Camera


class CameraServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8080,
                 camera: Camera = None, username: str = '', password: str = ''):
        self.host = host
        self.port = port
        self.camera = camera or Camera()
        self.username = username
        self.password = password
        self.app = Flask(__name__)
        self.app.config['BASIC_AUTH_USERNAME'] = username
        self.app.config['BASIC_AUTH_PASSWORD'] = password
        self.auth = BasicAuth(self.app)

    def _route_index(self):
        return render_template('index.html')

    def _route_stream(self):
        @self.auth.required
        def get():
            return Response(self.camera.get_stream(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        return get()

    def run(self):
        self.app.add_url_rule('/', '/', self._route_index)
        self.app.add_url_rule('/stream', '/stream', self._route_stream)
        self.app.run(host=self.host, port=self.port,
                     debug=False, threaded=True)
