import torch
from ultralytics import YOLO
import os

def train_human_detection_model():
    """
    Train a YOLOv8 model for human detection in disaster scenarios
    """
    
    # Check if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Load a pretrained YOLOv8 model (we'll use the nano version for faster training)
    model = YOLO('yolov8n.pt')
    
    # Set up output directories
    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(project_dir, 'training_outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    # Training parameters
    training_params = {
        'data': 'data.yaml',  # Path to our dataset configuration file
        'epochs': 50,         # Number of training epochs
        'imgsz': 640,         # Input image size
        'batch': 16,          # Batch size
        'project': output_dir,  # Base directory for outputs
        'name': 'human_detection_disaster',  # Name of the training run
        'device': device,     # Device to use for training
        'verbose': True,      # Print detailed training information
        'exist_ok': True      # Overwrite existing run if needed
    }
    
    # Train the model
    print("Starting training...")
    print(f"Outputs will be saved to: {os.path.join(output_dir, 'human_detection_disaster')}")
    results = model.train(**training_params)
    
    # The best model is automatically saved in the run directory
    # Get the path to the best model
    best_model_path = os.path.join(output_dir, 'human_detection_disaster', 'weights', 'best.pt')
    
    # Also save a copy in the project root for easy access
    model_copy_path = os.path.join(project_dir, 'human_detection_disaster_model.pt')
    if os.path.exists(best_model_path):
        import shutil
        shutil.copy2(best_model_path, model_copy_path)
        print(f"\nBest model copied to: {model_copy_path}")
        print(f"Full training results in: {os.path.join(output_dir, 'human_detection_disaster')}")
    
    return model

def validate_model(model_path=None):
    """
    Validate the trained model on the validation set
    """
    if model_path is None:
        # Default to model in project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(project_dir, 'human_detection_disaster_model.pt')
    
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return None
    
    # Load the trained model
    model = YOLO(model_path)
    
    # Validate the model
    print("Starting validation...")
    results = model.val(data='data.yaml')
    
    return results

def detect_humans_in_image(model_path, image_path, conf_threshold=0.5):
    """
    Detect humans in a single image using the trained model
    
    Args:
        model_path: Path to the trained model weights
        image_path: Path to the image to analyze
        conf_threshold: Confidence threshold for detections (0-1)
    """
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return None
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None
    
    # Load the trained model
    model = YOLO(model_path)
    
    # Perform detection
    results = model(image_path, conf=conf_threshold)
    
    # Display results
    results[0].show()
    
    # Print detection statistics
    detections = results[0].boxes
    print(f"\nDetected {len(detections)} humans with confidence >= {conf_threshold}")
    
    return results

if __name__ == "__main__":
    # Train the model
    trained_model = train_human_detection_model()
    
    # Validate the model
    # Use the path in project root
    project_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_dir, 'human_detection_disaster_model.pt')
    
    if os.path.exists(model_path):
        validation_results = validate_model(model_path)
        print("\nTraining and validation completed!")
        print(f"Model ready at: {model_path}")
    else:
        print("\nTraining completed but model file not found!")
        print("Check the training_outputs directory for the weights.")