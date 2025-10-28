"""
Complete Pipeline for Human Detection in Disaster Scenarios
This script provides a complete workflow for training, evaluating, and using 
a human detection model for disaster response scenarios.
"""

import os
import subprocess
import sys

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'torch',
        'ultralytics',
        'opencv-python',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:", missing_packages)
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def train_model():
    """Train the human detection model"""
    print("=== TRAINING MODEL ===")
    try:
        # Import and run training
        from train_human_detection import train_human_detection_model
        model = train_human_detection_model()
        print("Model training completed successfully!")
        return True
    except Exception as e:
        print(f"Error during training: {e}")
        return False

def evaluate_model():
    """Evaluate the trained model"""
    print("=== EVALUATING MODEL ===")
    try:
        # Import and run evaluation
        from evaluate_model import evaluate_model
        results = evaluate_model()
        print("Model evaluation completed successfully!")
        return True
    except Exception as e:
        print(f"Error during evaluation: {e}")
        return False

def visualize_dataset():
    """Visualize dataset samples"""
    print("=== VISUALIZING DATASET ===")
    try:
        # Import and run visualization
        from visualize_dataset import analyze_dataset_statistics, visualize_sample_images
        analyze_dataset_statistics('.')
        visualize_sample_images('.', split='train', num_samples=6)
        print("Dataset visualization completed successfully!")
        return True
    except Exception as e:
        print(f"Error during visualization: {e}")
        return False

def run_inference_example():
    """Run an inference example"""
    print("=== RUNNING INFERENCE EXAMPLE ===")
    try:
        # Check if model exists in project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(project_dir, 'human_detection_disaster_model.pt')
        if not os.path.exists(model_path):
            print("Trained model not found. Please train the model first.")
            return False
            
        # Import inference functions
        from inference import load_model
        model = load_model(model_path)
        if model:
            print("Inference example ready. Use the inference.py script for actual detection.")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error during inference setup: {e}")
        return False

def main():
    """Main pipeline execution"""
    print("HUMAN DETECTION IN DISASTER SCENARIOS - COMPLETE PIPELINE")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Show dataset information
    print("\n1. DATASET ANALYSIS")
    success = visualize_dataset()
    if not success:
        print("Dataset analysis failed. Continuing with other steps...")
    
    # Train model
    print("\n2. MODEL TRAINING")
    success = train_model()
    if not success:
        print("Model training failed. Skipping evaluation...")
        return
    
    # Evaluate model
    print("\n3. MODEL EVALUATION")
    success = evaluate_model()
    if not success:
        print("Model evaluation failed. Continuing...")
    
    # Setup inference
    print("\n4. INFERENCE SETUP")
    success = run_inference_example()
    if success:
        print("\nPipeline completed successfully!")
        print("\nNEXT STEPS:")
        print("- Use 'inference.py' to detect humans in new images or videos")
        print("- Check 'model_evaluation_report.json' for detailed metrics")
        print("- Check performance charts in 'performance_charts.png'")
        print("- View sample visualizations in 'train_samples.png'")
    else:
        print("\nPipeline completed with some issues.")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    main()