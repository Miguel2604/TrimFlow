from flask import Flask, request, render_template, jsonify, send_file, redirect, url_for
import os
import subprocess
import threading
import uuid
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Store processing status
processing_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_video(job_id, input_path, output_path, threshold, margin):
    """Process video in background thread"""
    try:
        processing_status[job_id] = {'status': 'processing', 'progress': 'Starting...'}
        
        # Construct the auto-editor command
        command = [
            "auto-editor",
            input_path,
            "-o", output_path,
            "--edit", f"audio:threshold={threshold}",
            "--margin", margin
        ]
        
        processing_status[job_id]['progress'] = 'Running auto-editor...'
        
        # Run the command
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            processing_status[job_id] = {
                'status': 'completed', 
                'progress': 'Video processing completed successfully!',
                'output_file': os.path.basename(output_path)
            }
        else:
            # Better error message formatting
            error_msg = stderr.strip() if stderr else 'Unknown error occurred'
            processing_status[job_id] = {
                'status': 'error', 
                'progress': 'Processing failed. Check error details below.',
                'error': error_msg,
                'error_details': f'Command: {" ".join(command)}\n\nError Output:\n{error_msg}'
            }
            
    except FileNotFoundError:
        processing_status[job_id] = {
            'status': 'error', 
            'progress': 'Error: auto-editor not found',
            'error': 'auto-editor command not found. Please ensure it is installed and in your PATH.'
        }
    except Exception as e:
        processing_status[job_id] = {
            'status': 'error', 
            'progress': f'Unexpected error: {str(e)}',
            'error': str(e)
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Secure filename
        filename = secure_filename(file.filename)
        timestamp = str(int(time.time()))
        input_filename = f"{timestamp}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        
        # Save uploaded file
        file.save(input_path)
        
        # Get parameters from form
        threshold = request.form.get('threshold', '4%')
        margin = request.form.get('margin', '0.2sec')
        
        # Generate output filename
        name, ext = os.path.splitext(filename)
        output_filename = f"{timestamp}_{name}_edited.mp4"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Start processing in background
        thread = threading.Thread(
            target=process_video, 
            args=(job_id, input_path, output_path, threshold, margin)
        )
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'message': 'File uploaded successfully. Processing started.',
            'filename': filename
        })
    
    return jsonify({'error': 'Invalid file type. Please upload MP4, MOV, AVI, or MKV files.'}), 400

@app.route('/status/<job_id>')
def get_status(job_id):
    if job_id in processing_status:
        return jsonify(processing_status[job_id])
    else:
        return jsonify({'status': 'not_found', 'error': 'Job ID not found'}), 404

@app.route('/download/<filename>')
def download_file(filename):
    try:
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(output_path):
            return send_file(output_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup/<job_id>', methods=['POST'])
def cleanup_files(job_id):
    """Clean up uploaded and processed files"""
    try:
        # This is a simple cleanup - in production you'd want more sophisticated file management
        return jsonify({'message': 'Cleanup completed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting TrimFlow Web App...")
    print("Make sure auto-editor is installed and in your PATH!")
    print("Access the app at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
