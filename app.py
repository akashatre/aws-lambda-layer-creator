from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
import shutil
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Directory where Lambda layers will be stored
LAYER_DIR = "layers"

def check_pypi_package(package_name):
    """Check if a package exists on PyPI."""
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    return response.status_code == 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-layer', methods=['POST'])
def create_layer():
    layer_name = request.form['layer_name'].lower()

    # Validate if the package exists on PyPI
    if not check_pypi_package(layer_name):
        flash(f"Layer '{layer_name}' is not available.")
        return redirect(url_for('index'))

    # Create a directory for the layer
    layer_path = os.path.join(LAYER_DIR, layer_name)
    if not os.path.exists(layer_path):
        os.makedirs(layer_path)

    # Create requirements.txt
    with open(os.path.join(layer_path, 'requirements.txt'), 'w') as f:
        f.write(layer_name)

    # Install dependencies
    os.system(f'pip install -r {os.path.join(layer_path, "requirements.txt")} -t {os.path.join(layer_path, "python/lib/python3.10/site-packages/")}')
    
    # Zip the layer directory
    zip_path = f"{layer_name}.zip"
    shutil.make_archive(layer_name, 'zip', layer_path)

    # Move the zipped file to layers directory
    shutil.move(f"{layer_name}.zip", os.path.join(LAYER_DIR, zip_path))

    return redirect(url_for('download_layer', layer_name=zip_path))

@app.route('/download/<layer_name>')
def download_layer(layer_name):
    return send_file(os.path.join(LAYER_DIR, layer_name), as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(LAYER_DIR):
        os.makedirs(LAYER_DIR)
    app.run(debug=True)
