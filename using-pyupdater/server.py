from flask import Flask, render_template, request
import os
import subprocess
import PyUpdater
from PyUpdater.server.api import ServerUpdate

app = Flask(__name__)

# PyUpdater configuration
CONF_FILE = 'pyupdater.conf'
server_config = PyUpdater.settings.load_config(CONF_FILE)

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    server_updater = ServerUpdate(server_config)
    server_updater.process_update_request(request.files)
    return 'Update processed.'

if __name__ == '__main__':
    app.run()