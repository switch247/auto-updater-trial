from flask import Flask, send_from_directory, jsonify
import json
import os

app = Flask(__name__)


@app.route('/checklatest')
def check_latest_version():
    version_file = 'version.json'
    if os.path.isfile(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            version_data = json.load(f)
            return jsonify(version_data)
    else:
        return jsonify({'error': 'Version file not found'}), 404
    

@app.route('/update/<filename>')
def get_update(filename):
    updates_directory = './updater'
    files = os.listdir(updates_directory)
    file_list = [f for f in files if os.path.isfile(os.path.join(updates_directory, f))]
    print(file_list)
    file_path = os.path.join(updates_directory, filename)
    if os.path.isfile(file_path):
        return send_from_directory(updates_directory, filename)
    else:
        print({'error': f'File not found: {filename}'})
        return jsonify({'error': f'File not found: {filename}'}), 404


if __name__ == '__main__':
    app.run(port=5000)
