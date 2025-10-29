import cv2
import os
import numpy as np
import random
import matplotlib.pyplot as plt
from pathlib import Path

def load_yolo_labels(label_path, img_width, img_height):
    """
    Load YOLO format labels and convert to pixel coordinates
    
    Args:
        label_path: Path to the label file
        img_width: Width of the image
        img_height: Height of the image
    
    Returns:
        boxes: List of bounding boxes in [x1, y1, x2, y2] format
        classes: List of class IDs
    """
    boxes = []
    classes = []
    
    if not os.path.exists(label_path):
        return boxes, classes
    
    with open(label_path, 'r') as f:
        for line in f.readlines():
            data = line.strip().split()
            if len(data) == 5:
                class_id, x_center, y_center, width, height = map(float, data)
                
                x_center *= img_width
                y_center *= img_height
                width *= img_width
                height *= img_height
                
                x1 = int(x_center - width / 2)
                y1 = int(y_center - height / 2)
                x2 = int(x_center + width / 2)
                y2 = int(y_center + height / 2)
                
                boxes.append([x1, y1, x2, y2])
                classes.append(int(class_id))
    
    return boxes, classes

def draw_bounding_boxes(image, boxes, classes, class_names=None):
    """
    Draw bounding boxes on an image
    
    Args:
        image: Input image
        boxes: List of bounding boxes in [x1, y1, x2, y2] format
        classes: List of class IDs
        class_names: Dictionary mapping class IDs to names
    
    Returns:
        image: Image with bounding boxes drawn
    """
    image_copy = image.copy()
    
    colors = [
        (0, 255, 0),    
        (255, 0, 0),   
        (0, 0, 255),    
        (255, 255, 0),  
        (255, 0, 255), 
        (0, 255, 255),  
    ]
    
    for i, (box, class_id) in enumerate(zip(boxes, classes)):
        x1, y1, x2, y2 = box
        color = colors[class_id % len(colors)]
        
        cv2.rectangle(image_copy, (x1, y1), (x2, y2), color, 2)
        
        if class_names:
            label = class_names.get(class_id, f"Class {class_id}")
        else:
            label = f"Class {class_id}"
        
        cv2.putText(image_copy, label, (x1, y1 - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return image_copy

def visualize_sample_images(dataset_path, split='train', num_samples=9):
    """
    Visualize sample images with their annotations
    
    Args:
        dataset_path: Path to the dataset root
        split: Dataset split to visualize ('train', 'val', or 'test')
        num_samples: Number of samples to visualize
    """
    images_path = os.path.join(dataset_path, split, 'images')
    labels_path = os.path.join(dataset_path, split, 'labels')
    
    image_files = [f for f in os.listdir(images_path) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    sampled_files = random.sample(image_files, min(num_samples, len(image_files)))
    
    class_names = {0: "Human"}
    notes_path = os.path.join(dataset_path, 'notes.json')
    if os.path.exists(notes_path):
        try:
            with open(notes_path, 'r') as f:
                notes = json.load(f)
                if 'categories' in notes:
                    class_names = {cat['id']: cat['name'] for cat in notes['categories']}
        except:
            pass
    
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    axes = axes.ravel()
    
    for i, image_file in enumerate(sampled_files):
        image_path = os.path.join(images_path, image_file)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        img_height, img_width = image.shape[:2]
        
        label_file = os.path.splitext(image_file)[0] + '.txt'
        label_path = os.path.join(labels_path, label_file)
        boxes, classes = load_yolo_labels(label_path, img_width, img_height)
        
        image_with_boxes = draw_bounding_boxes(image, boxes, classes, class_names)
        
        axes[i].imshow(image_with_boxes)
        axes[i].set_title(f"{split.capitalize()}: {image_file}")
        axes[i].axis('off')
        
        print(f"Image: {image_file}")
        print(f"  Dimensions: {img_width}x{img_height}")
        print(f"  Objects detected: {len(boxes)}")
        for j, (box, class_id) in enumerate(zip(boxes, classes)):
            class_name = class_names.get(class_id, f"Class {class_id}")
            print(f"    {j+1}. {class_name} at [{box[0]}, {box[1]}, {box[2]}, {box[3]}]")
        print()
    
    for i in range(len(sampled_files), 9):
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.savefig(f'{split}_samples.png')
    plt.show()
    
    print(f"Sample images saved to {split}_samples.png")

def analyze_dataset_statistics(dataset_path):
    """
    Analyze dataset statistics
    
    Args:
        dataset_path: Path to the dataset root
    """
    splits = ['train', 'val', 'test']
    
    print("=== DATASET STATISTICS ===")
    
    for split in splits:
        images_path = os.path.join(dataset_path, split, 'images')
        labels_path = os.path.join(dataset_path, split, 'labels')
        
        image_files = [f for f in os.listdir(images_path) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        label_files = [f for f in os.listdir(labels_path) 
                       if f.lower().endswith('.txt')]
        
        total_objects = 0
        for label_file in label_files:
            label_path = os.path.join(labels_path, label_file)
            if os.path.exists(label_path):
                with open(label_path, 'r') as f:
                    total_objects += len(f.readlines())
        
        print(f"{split.capitalize()} set:")
        print(f"  Images: {len(image_files)}")
        print(f"  Label files: {len(label_files)}")
        print(f"  Total objects: {total_objects}")
        if len(image_files) > 0:
            print(f"  Avg objects per image: {total_objects/len(image_files):.2f}")
        print()

if __name__ == "__main__":
    import json
    
    dataset_path = '.'
    
    analyze_dataset_statistics(dataset_path)
    
    for split in ['train', 'val']:
        try:
            print(f"\nVisualizing {split} samples...")
            visualize_sample_images(dataset_path, split=split, num_samples=9)
        except Exception as e:
            print(f"Error visualizing {split} samples: {e}")
    
    print("Dataset visualization completed!")