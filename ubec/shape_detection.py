import cv2  # OpenCV Library
import tkinter as tk
import numpy as np
from tkinter import filedialog
import os
from typing import Any

def get_project_root():
    """Get the absolute path to the project root directory"""
    current_file = os.path.abspath(__file__)  # Get the path to this file
    return os.path.dirname(os.path.dirname(current_file))  # Go up two levels

def load_reference_shapes(folder_name: str) -> dict[str, np.ndarray[Any, np.dtype[np.float64]]]:
    """Load reference shapes from the shapes folder in project root"""
    project_root = get_project_root()
    folder_path = os.path.join(project_root, folder_name)
    
    # Check if folder existss
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Shapes folder not found at {folder_path}")
    
    reference_shapes: dict[str, np.ndarray[Any, np.dtype[np.float64]]] = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            label = os.path.splitext(filename)[0]
            ref_image_path = os.path.join(folder_path, filename)
            
            # Check if file exists
            if not os.path.exists(ref_image_path):
                print(f"Warning: Reference image {filename} not found")
                continue
                
            ref_image = cv2.imread(ref_image_path, cv2.IMREAD_GRAYSCALE)

            _, ref_thresh = cv2.threshold(ref_image, 127, 255, cv2.THRESH_BINARY)
            ref_contours, _ = cv2.findContours(ref_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if ref_contours:
                reference_shapes[label] = np.array(ref_contours[0], dtype=np.float64)
            else:
                print(f"Warning: No contours found in {filename}")
    
    if not reference_shapes:
        raise ValueError("No reference shapes were loaded")
        
    return reference_shapes

def process_image(image_path: str) -> None:
    # Load reference shape contours from folder
    reference_shapes: dict[str, np.ndarray[Any, np.dtype[np.float64]]] = load_reference_shapes("ubec//shapes")

    # Read the image
    image = cv2.imread(filename=image_path)

    # Convert to grayscale if not already
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
    # Thresholding
    _, thresh_image = cv2.threshold(src=gray_image, thresh=180, maxval=255, type=cv2.THRESH_BINARY)

     # Find contours - use RETR_EXTERNAL to only get outer contours
    contours, _ = cv2.findContours(
        image=thresh_image, 
        mode=cv2.RETR_EXTERNAL, 
        method=cv2.CHAIN_APPROX_SIMPLE
    )

     # Filter contours by area to remove noise
    min_area = 100  # Adjust this value based on your text size
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
    total_contours = len(contours)
    print(f"Total text components detected: {total_contours}")

     # Create a copy for visualization
    result_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    cv2.putText(result_image, f"Total components: {total_contours}", 
                (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 1)

    for _, contour in enumerate(contours):
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        
        # Draw rectangle around text component
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Compare with reference shapes
        best_match = None
        lowest_score = float('inf')

        for label, ref_contour in reference_shapes.items():
            score = cv2.matchShapes(contour, ref_contour, cv2.CONTOURS_MATCH_I1, 0.0)
            if score < lowest_score:
                lowest_score = score
                best_match = label

        # Label the text component
        if best_match and lowest_score < 0.15:  # Adjust threshold as needed
            cv2.putText(result_image, best_match, 
                       (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 0, 0), 1)

    # Save the result
    output_path = os.path.join(os.path.dirname(image_path), "detected_text.png")
    cv2.imwrite(output_path, result_image)
    print(f"Result saved to: {output_path}")

def select_image() -> None:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
    )
    if file_path:
        process_image(file_path)

if __name__ == "__main__":
    select_image()
