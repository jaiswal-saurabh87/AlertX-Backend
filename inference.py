import torch
from ultralytics import YOLO
import cv2
import numpy as np
import os

def load_model(model_path=None):
    """
    Load the trained human detection model
    """
    if model_path is None:
        # Default to model in project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(project_dir, 'human_detection_disaster_model.pt')
    
    try:
        model = YOLO(model_path)
        print(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def detect_humans_in_image(model, image_path, confidence_threshold=0.5, save_output=True):
    """
    Detect humans in a single image
    
    Args:
        model: Loaded YOLO model
        image_path: Path to the input image
        confidence_threshold: Minimum confidence threshold for detections
        save_output: Whether to save the output image with bounding boxes
    
    Returns:
        results: Detection results
    """
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return None
    
    # Perform detection
    results = model(image_path, conf=confidence_threshold)
    
    # Display results
    result_image = results[0].plot()
    
    # Save output if requested
    if save_output:
        output_path = image_path.replace('.jpg', '_detected.jpg').replace('.png', '_detected.png')
        cv2.imwrite(output_path, result_image)
        print(f"Output saved to: {output_path}")
    
    # Show image
    cv2.imshow('Human Detection Results', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return results

def detect_humans_in_video(model, video_path, confidence_threshold=0.5, save_output=True):
    """
    Detect humans in a video
    
    Args:
        model: Loaded YOLO model
        video_path: Path to the input video
        confidence_threshold: Minimum confidence threshold for detections
        save_output: Whether to save the output video with bounding boxes
    """
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Initialize video writer if saving output
    out = None
    if save_output:
        output_path = video_path.replace('.mp4', '_detected.mp4').replace('.avi', '_detected.avi')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        print(f"Output video will be saved to: {output_path}")
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Perform detection on frame
        results = model(frame, conf=confidence_threshold)
        result_frame = results[0].plot()
        
        # Write frame to output video
        if out is not None:
            out.write(result_frame)
        
        # Display frame
        cv2.imshow('Human Detection in Video', result_frame)
        
        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames...")
    
    # Release everything
    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()
    
    print(f"Video processing completed. Total frames processed: {frame_count}")

def batch_process_images(model, image_folder, confidence_threshold=0.5, save_output=True):
    """
    Process all images in a folder
    
    Args:
        model: Loaded YOLO model
        image_folder: Path to folder containing images
        confidence_threshold: Minimum confidence threshold for detections
        save_output: Whether to save the output images with bounding boxes
    """
    if not os.path.exists(image_folder):
        print(f"Image folder not found: {image_folder}")
        return
    
    # Supported image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    # Create output folder if saving results
    output_folder = None
    if save_output:
        output_folder = os.path.join(image_folder, 'detected')
        os.makedirs(output_folder, exist_ok=True)
    
    # Process each image
    image_files = [f for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in image_extensions]
    
    for i, image_file in enumerate(image_files):
        image_path = os.path.join(image_folder, image_file)
        print(f"Processing image {i+1}/{len(image_files)}: {image_file}")
        
        try:
            # Perform detection
            results = model(image_path, conf=confidence_threshold)
            result_image = results[0].plot()
            
            # Save output if requested
            if save_output and output_folder is not None:
                output_path = os.path.join(output_folder, image_file)
                cv2.imwrite(output_path, result_image)
                print(f"  Saved detection result to: {output_path}")
                
        except Exception as e:
            print(f"  Error processing {image_file}: {e}")
    
    print(f"Batch processing completed. Processed {len(image_files)} images.")

if __name__ == "__main__":
    # Load the model
    model = load_model()
    
    if model is None:
        print("Failed to load model. Please ensure the model file exists.")
        exit(1)
    
    # Example usage:
    # 1. Detect humans in a single image
    # detect_humans_in_image(model, "path/to/your/image.jpg")
    
    # 2. Detect humans in a video
    # detect_humans_in_video(model, "path/to/your/video.mp4")
    
    # 3. Batch process images in a folder
    # batch_process_images(model, "path/to/your/image/folder")
    
    print("Model loaded successfully. You can now use the detection functions.")
    print("Example usage:")
    print("  detect_humans_in_image(model, 'path/to/image.jpg')")
    print("  detect_humans_in_video(model, 'path/to/video.mp4')")
    print("  batch_process_images(model, 'path/to/image/folder')")