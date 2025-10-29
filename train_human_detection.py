import torch
from ultralytics import YOLO
import os

def train_human_detection_model():
    """
    Train a YOLOv8 model for human detection in disaster scenarios
    """
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    

    model = YOLO('yolov8n.pt')
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(project_dir, 'training_outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    training_params = {
        'data': 'data.yaml',  
        'epochs': 50,        
        'imgsz': 640,         
        'batch': 16,          
        'project': output_dir, 
        'name': 'human_detection_disaster',  
        'device': device,    
        'verbose': True,    
        'exist_ok': True      
    }
    
    print("Starting training...")
    print(f"Outputs will be saved to: {os.path.join(output_dir, 'human_detection_disaster')}")
    results = model.train(**training_params)
    

    best_model_path = os.path.join(output_dir, 'human_detection_disaster', 'weights', 'best.pt')
    
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
        project_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(project_dir, 'human_detection_disaster_model.pt')
    
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return None
    
    model = YOLO(model_path)
    
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
    
    model = YOLO(model_path)
    
    results = model(image_path, conf=conf_threshold)
    
    results[0].show()
    
    detections = results[0].boxes
    print(f"\nDetected {len(detections)} humans with confidence >= {conf_threshold}")
    
    return results

if __name__ == "__main__":
    trained_model = train_human_detection_model()
    

    project_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_dir, 'human_detection_disaster_model.pt')
    
    if os.path.exists(model_path):
        validation_results = validate_model(model_path)
        print("\nTraining and validation completed!")
        print(f"Model ready at: {model_path}")
    else:
        print("\nTraining completed but model file not found!")
        print("Check the training_outputs directory for the weights.")