import os
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from main import query_answer
from textloader import process_all_files_in_uploader

app = Flask(__name__, template_folder='../templates', static_folder='../static')
UPLOAD_FOLDER = 'uploader'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})  # Allow requests from your React app's origin

# Keep track of the uploaded files
uploaded_files = []
processed_files = []  # Store the names of files that have been processed

# Lock to ensure thread safety when processing files
file_processing_lock = False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def get_response():
    data = request.get_json()
    user_input = data['input']
    bot_response = query_answer(user_input)
    return jsonify({'response': bot_response})


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global uploaded_files, file_processing_lock
    if request.method == 'POST':
        files = request.files.getlist('files')

        if not files:
            return jsonify({'error': 'No files provided'})

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Check if the file has already been processed
                if filename in processed_files:
                    print(f"File '{filename}' has already been processed. Skipping...")
                    continue

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_files.append(filename)
                print(f"File '{filename}' has been uploaded.")

                # Process the uploaded files
                if not file_processing_lock:
                    file_processing_lock = True
                    process_all_files_in_uploader()
                    file_processing_lock = False

        if uploaded_files:
            return jsonify({'message': f'{len(uploaded_files)} files uploaded successfully'})
        else:
            return jsonify({'error': 'No valid files uploaded'})
    else:
        return render_template('fileuploader.html')


if __name__ == '__main__':
    app.run(port=8000)
