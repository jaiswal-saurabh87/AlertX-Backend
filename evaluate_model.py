import torch
from ultralytics import YOLO
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

def evaluate_model(model_path=None, data_config='data.yaml'):
    """
    Evaluate the trained model on the test set and generate performance metrics
    """
    if model_path is None:
        # Default to model in project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(project_dir, 'human_detection_disaster_model.pt')
    
    print("Loading model...")
    model = YOLO(model_path)
    
    print("Running evaluation on test set...")
    # Run evaluation
    results = model.val(data=data_config, split='test')
    
    # Print results
    print("\n=== MODEL EVALUATION RESULTS ===")
    print(f"mAP50: {results.box.map50:.4f}")
    print(f"mAP50-95: {results.box.map:.4f}")
    print(f"Precision: {results.box.p.mean():.4f}")
    print(f"Recall: {results.box.r.mean():.4f}")
    print(f"F1-Score: {results.box.f1.mean():.4f}")
    
    # Per-class results
    print("\n=== PER-CLASS METRICS ===")
    names = model.names
    for i, name in enumerate(names):
        if i < len(results.box.p):
            print(f"{name}:")
            print(f"  Precision: {results.box.p[i]:.4f}")
            print(f"  Recall: {results.box.r[i]:.4f}")
            print(f"  F1-Score: {results.box.f1[i]:.4f}")
            print(f"  mAP50: {results.box.ap50[i]:.4f}")
    
    return results

def plot_performance_charts(results, save_path='performance_charts.png'):
    """
    Plot performance charts for the model
    """
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Model Performance Metrics', fontsize=16)
    
    # Bar chart for mAP, Precision, Recall, F1
    metrics = ['mAP50', 'Precision', 'Recall', 'F1-Score']
    values = [results.box.map50, results.box.p.mean(), results.box.r.mean(), results.box.f1.mean()]
    
    axes[0, 0].bar(metrics, values, color=['blue', 'green', 'red', 'orange'])
    axes[0, 0].set_title('Overall Performance Metrics')
    axes[0, 0].set_ylim(0, 1)
    for i, v in enumerate(values):
        axes[0, 0].text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
    
    # Precision-Recall curve (simplified)
    if len(results.box.p) > 0 and len(results.box.r) > 0:
        axes[0, 1].scatter(results.box.r, results.box.p, alpha=0.7)
        axes[0, 1].set_xlabel('Recall')
        axes[0, 1].set_ylabel('Precision')
        axes[0, 1].set_title('Precision-Recall Tradeoff')
        axes[0, 1].set_xlim(0, 1)
        axes[0, 1].set_ylim(0, 1)
        axes[0, 1].grid(True)
    
    # Class-wise precision
    classes = list(range(len(results.box.p))) if len(results.box.p) > 0 else []
    if len(classes) > 0:
        axes[1, 0].bar(classes, results.box.p, color='skyblue')
        axes[1, 0].set_title('Class-wise Precision')
        axes[1, 0].set_xlabel('Class')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].set_ylim(0, 1)
    
    # Class-wise recall
    if len(classes) > 0:
        axes[1, 1].bar(classes, results.box.r, color='lightcoral')
        axes[1, 1].set_title('Class-wise Recall')
        axes[1, 1].set_xlabel('Class')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Performance charts saved to {save_path}")

def generate_detailed_report(results, model):
    """
    Generate a detailed evaluation report
    """
    report = {
        "model_info": {
            "model_type": "YOLOv8",
            "classes": list(model.names.values()),
            "date": str(np.datetime64('now'))
        },
        "overall_metrics": {
            "mAP50": float(results.box.map50),
            "mAP50_95": float(results.box.map),
            "precision": float(results.box.p.mean()),
            "recall": float(results.box.r.mean()),
            "f1_score": float(results.box.f1.mean())
        },
        "class_metrics": {}
    }
    
    names = model.names
    for i, name in enumerate(names):
        if i < len(results.box.p):
            report["class_metrics"][name] = {
                "precision": float(results.box.p[i]),
                "recall": float(results.box.r[i]),
                "f1_score": float(results.box.f1[i]),
                "ap50": float(results.box.ap50[i])
            }
    
    # Save report to JSON
    with open('model_evaluation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("Detailed evaluation report saved to model_evaluation_report.json")
    return report

if __name__ == "__main__":
    # Evaluate the model
    try:
        # Load model for additional information
        project_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(project_dir, 'human_detection_disaster_model.pt')
        model = YOLO(model_path)
        
        results = evaluate_model(model_path)
        
        # Generate detailed report
        report = generate_detailed_report(results, model)
        
        # Plot performance charts
        plot_performance_charts(results)
        
        print("\nEvaluation completed successfully!")
        print("Check the following files:")
        print("  - model_evaluation_report.json (Detailed metrics)")
        print("  - performance_charts.png (Visual performance charts)")
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        print("Please ensure the model file and data configuration exist.")