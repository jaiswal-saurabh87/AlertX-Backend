import os
import sys
import json
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import torch
import cv2
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import PORT

from inference import load_model

app = Flask(__name__)
CORS(app)  
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

model = load_model()

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def process_image(filepath, confidence_threshold=0.5):
    """Process an image file and return detection results"""
    if model is None:
        raise Exception("Model not loaded")
    
    results = model(filepath, conf=confidence_threshold)
    
    result_data = results[0]
    boxes = result_data.boxes
    
    detections = []
    if boxes is not None:
        for box in boxes:
            xyxy = box.xyxy[0].cpu().numpy()
            confidence = float(box.conf[0].cpu().numpy())
            class_id = int(box.cls[0].cpu().numpy())
            
            detections.append({
                'bbox': {
                    'x1': float(xyxy[0]),
                    'y1': float(xyxy[1]),
                    'x2': float(xyxy[2]),
                    'y2': float(xyxy[3])
                },
                'confidence': confidence,
                'class_id': class_id,
                'class_name': 'Human' if class_id == 0 else f'Class {class_id}'
            })
    
    result_image = result_data.plot()
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    processed_filename = f"{name}_detected{ext}"
    processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
    cv2.imwrite(processed_filepath, result_image)
    
    return {
        'detections': detections,
        'processed_image': processed_filename,
        'count': len(detections)
    }

def process_video(filepath, confidence_threshold=0.5):
    """Process a video file and return detection results"""
    if model is None:
        raise Exception("Model not loaded")
    
    cap = cv2.VideoCapture(filepath)
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    processed_filename = f"{name}_detected{ext}"
    processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(processed_filepath, fourcc, fps, (width, height))
    
    frame_count = 0
    total_detections = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame, conf=confidence_threshold)
        result_frame = results[0].plot()
        
        boxes = results[0].boxes
        if boxes is not None:
            total_detections += len(boxes)
        
        out.write(result_frame)
        
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processed {frame_count}/{total_frames} frames...")
    
    cap.release()
    out.release()
    
    return {
        'processed_video': processed_filename,
        'total_frames': frame_count,
        'total_detections': total_detections,
        'avg_detections_per_frame': total_detections / frame_count if frame_count > 0 else 0
    }

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload a media file for processing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    is_image = allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS)
    is_video = allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS)
    
    if not (is_image or is_video):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        filename = file.filename or 'uploaded_file'
        secured_filename = secure_filename(filename)
        if not secured_filename:
            secured_filename = 'uploaded_file'
        
        name, ext = os.path.splitext(secured_filename)
        unique_filename = f"{name}_{uuid.uuid4().hex}{ext}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': unique_filename,
            'filepath': filepath,
            'type': 'image' if is_image else 'video'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_file():
    """Process an uploaded file"""
    data = request.get_json()
    
    if not data or 'filename' not in data:
        return jsonify({'error': 'Filename not provided'}), 400
    
    filename = data['filename']
    confidence_threshold = data.get('confidence_threshold', 0.5)
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        is_image = allowed_file(filename, ALLOWED_IMAGE_EXTENSIONS)
        is_video = allowed_file(filename, ALLOWED_VIDEO_EXTENSIONS)
        
        if is_image:
            result = process_image(filepath, confidence_threshold)
            return jsonify({
                'status': 'success',
                'type': 'image',
                'result': result
            }), 200
        elif is_video:
            result = process_video(filepath, confidence_threshold)
            return jsonify({
                'status': 'success',
                'type': 'video',
                'result': result
            }), 200
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/processed/<filename>')
def serve_processed_file(filename):
    """Serve processed files"""
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not loaded"
    return jsonify({
        'status': 'healthy',
        'model_status': model_status
    }), 200

if __name__ == '__main__':
    print("Starting Human Detection API Server...")
    if model is None:
        print("Warning: Model failed to load. API will start but processing will fail.")
    else:
        print("Model loaded successfully.")
    print(f"Server running on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)