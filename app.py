import os
import rawpy
import imageio
import multiprocessing
import time
from multiprocessing import Manager
from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Constants and Configuration
UPLOAD_FOLDER = os.path.abspath('uploads')
OUTPUT_FOLDER = os.path.abspath('outputs')
ALLOWED_EXTENSIONS = {'.nef', '.cr2', '.arw', '.raw', '.dng', '.raf', '.3fr', '.dcr', '.k25', '.kdc', '.mrw', '.pef', '.srw', '.x3f'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Configure Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5000 * 1024 * 1024  

def get_new_filename(counter, output_directory):
    counter['value'] += 1
    current_number = counter['value']
    filename = f'jpeg{current_number}.jpg'
    return os.path.join(output_directory, secure_filename(filename))

def process_raw(input_file, output_directory, counter):
    try:
        output_file = get_new_filename(counter, output_directory)
        with rawpy.imread(input_file) as raw:
            rgb = raw.postprocess()
            imageio.imsave(output_file, rgb)
        return os.path.basename(output_file)  # Return just the filename
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        return None

def process_images(input_directory, output_directory):
    raw_files = [
        os.path.join(input_directory, filename)
        for filename in os.listdir(input_directory)
        if os.path.splitext(filename.lower())[1] in ALLOWED_EXTENSIONS
    ]

    if not raw_files:
        raise Exception("No RAW files found")

    with Manager() as manager:
        counter = manager.dict()
        counter['value'] = 0
        
        num_processes = max(1, multiprocessing.cpu_count() - 1)
        processed_files = []

        with multiprocessing.Pool(processes=num_processes) as pool:
            results = []
            last_activity = time.time()

            for file in raw_files:
                results.append(pool.apply_async(process_raw, (file, output_directory, counter)))

            while results:
                for i in range(len(results) - 1, -1, -1):
                    if results[i].ready():
                        result = results[i].get()
                        if result:
                            processed_files.append(result)
                        results.pop(i)
                        last_activity = time.time()

                if time.time() - last_activity > 30:  # Increased timeout to 30 seconds
                    print("Timeout reached - no activity for 30 seconds")
                    pool.terminate()
                    break

                time.sleep(0.5)

        return processed_files

def clear_directory(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('files[]')
    uploaded_files = []
    
    clear_directory(UPLOAD_FOLDER)  # Clear previous uploads
    
    for file in files:
        if file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append(filename)

    return jsonify({'message': f'{len(uploaded_files)} files uploaded successfully'})

@app.route('/process', methods=['POST'])
def process_files():
    try:
        clear_directory(OUTPUT_FOLDER)  # Clear previous outputs
        
        processed_files = process_images(UPLOAD_FOLDER, OUTPUT_FOLDER)
        
        if processed_files:
            file_urls = []
            for filename in processed_files:
                file_url = url_for('download_file', filename=filename, _external=True)
                file_urls.append(file_url)
            
            return jsonify({
                'message': 'Files processed successfully',
                'files': processed_files,
                'urls': file_urls
            })
        else:
            return jsonify({'error': 'No files were processed successfully'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    try:
        return send_from_directory(
            app.config['OUTPUT_FOLDER'],
            filename,
            as_attachment=True,
            mimetype='image/jpeg'
        )
    except Exception as e:
        return jsonify({'error': f'Error serving file: {str(e)}'}), 404

if __name__ == '__main__':
    multiprocessing.freeze_support()
    app.run(debug=False)
