import os
import hashlib
import zipfile
from PIL import Image
from flask import Flask, render_template, request, send_file, jsonify
from bing_image_downloader import downloader
from werkzeug.utils import secure_filename
import threading
import webbrowser

# Get the absolute path of the current script
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Configuration
UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(STATIC_DIR, 'processed_images')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_image(image_path):
    with Image.open(image_path) as img:
        img = img.resize((256, 256)).convert('RGB')
        image_bytes = img.tobytes()
        return hashlib.md5(image_bytes).hexdigest()

def process_images(input_directory, output_directory, resize_dimensions, min_size=(100, 100)):
    hashes = {}
    processed_images = []

    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if os.path.isfile(file_path) and allowed_file(filename):
            try:
                with Image.open(file_path) as img:
                    if img.size[0] >= min_size[0] and img.size[1] >= min_size[1]:
                        image_hash = hash_image(file_path)
                        if image_hash not in hashes:
                            resized_img = img.resize(resize_dimensions)
                            output_path = os.path.join(output_directory, filename)
                            resized_img.save(output_path)
                            hashes[image_hash] = output_path
                            processed_images.append(filename)
            except Exception as e:
                print(f"Could not process {file_path}: {e}")

    return processed_images

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        limit = int(request.form.get('limit', 10))
        resize_width = int(request.form.get('resize_width', 128))
        resize_height = int(request.form.get('resize_height', 128))
        
        if query:
            download_folder = os.path.join(UPLOAD_FOLDER, secure_filename(query))
            downloader.download(query, limit=limit, output_dir=download_folder, adult_filter_off=False, force_replace=False, timeout=60, verbose=True)
            processed_images = process_images(download_folder, OUTPUT_FOLDER, (resize_width, resize_height))
            return render_template('index.html', images=processed_images, query=query, processing_complete=True)
    return render_template('index.html')

@app.route('/download_zip')
def download_zip():
    zip_path = os.path.join(app.root_path, 'processed_images.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(OUTPUT_FOLDER):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    return send_file(zip_path, as_attachment=True)

@app.route('/get_images')
def get_images():
    images = [f for f in os.listdir(OUTPUT_FOLDER) if allowed_file(f)]
    return jsonify(images)

@app.route('/reset', methods=['POST'])
def reset():
    # Clear the OUTPUT_FOLDER
    try:
        for filename in os.listdir(OUTPUT_FOLDER):
            file_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete each file
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=False)
