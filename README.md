# Human Detection in Disaster Scenarios

This project contains a machine learning model trained to detect humans in disaster scenarios such as earthquakes, floods, and building collapses.

## Dataset Structure

The dataset is organized in the following structure:
```
Veri Seti/
├── train_human_detection.py (Training script)
├── inference.py (Inference script)
├── evaluate_model.py (Model evaluation)
├── visualize_dataset.py (Dataset visualization)
├── run_complete_pipeline.py (Complete workflow)
├── setup_and_run.bat (Windows setup script)
└── requirements.txt (Dependencies)
```

## Label Format

The labels are in YOLO format:
- Each label file contains one line per object
- Each line has 5 values: `class_id center_x center_y width height`
- All values are normalized between 0 and 1
- Class ID 0 represents "Human"

## Installation

### Option 1: Manual Installation
1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Windows Setup
On Windows systems, simply run the setup script:
```bash
setup_and_run.bat
```
This will automatically install dependencies and run the complete pipeline.

## Training

### Option 1: Individual Script
To train the model, run:
```bash
python train_human_detection.py
```

This will:
1. Load a pretrained YOLOv8 model
2. Train it on the disaster scenario dataset
3. Save the trained model as `human_detection_disaster_model.pt`
4. Validate the model on the validation set

### Option 2: Complete Pipeline
Run the complete pipeline that includes dataset analysis, training, and evaluation:
```bash
python run_complete_pipeline.py
```

## Using the Model

### Option 1: Simple Detection
After training, you can use the model to detect humans in new images:

```python
from train_human_detection import detect_humans_in_image

# Detect humans in an image
results = detect_humans_in_image('human_detection_disaster_model.pt', 'path/to/image.jpg')
```

### Option 2: Advanced Inference
Use the dedicated inference script for more advanced detection capabilities:

```python
from inference import load_model, detect_humans_in_image, detect_humans_in_video

# Load the trained model
model = load_model()

# Detect humans in a single image
results = detect_humans_in_image(model, 'path/to/image.jpg')

# Detect humans in a video
detect_humans_in_video(model, 'path/to/video.mp4')

# Batch process images in a folder
batch_process_images(model, 'path/to/image/folder')
```

## Additional Scripts

The repository includes several additional scripts for comprehensive analysis:

1. `visualize_dataset.py` - Analyze and visualize dataset samples
2. `evaluate_model.py` - Detailed model evaluation with performance charts
3. `inference.py` - Advanced inference capabilities for images and videos
4. `run_complete_pipeline.py` - Execute the complete workflow
5. `setup_and_run.bat` - Windows batch script for easy setup

## Model Architecture

The model is based on YOLOv8 (You Only Look Once version 8), which is a state-of-the-art real-time object detection system. It's particularly well-suited for disaster response scenarios where quick detection is crucial.

## Performance

The model is trained to detect humans in various disaster scenarios:
- Earthquakes
- Floods
- Building collapses
- Fire incidents

The validation process will provide metrics on the model's performance including precision, recall, and mAP (mean Average Precision).

## Generated Outputs

After running the pipeline, you'll find these files:
- `human_detection_disaster_model.pt` - Trained model
- `model_evaluation_report.json` - Detailed evaluation metrics
- `performance_charts.png` - Visual performance charts
- `train_samples.png` - Sample annotated images
- `*.txt` detection results in output folders
