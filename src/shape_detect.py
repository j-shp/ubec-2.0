import cv2
import os
import numpy as np
from tkinter import filedialog, Tk

def get_project_root():
    """Get the absolute path to the project root directory"""
    current_file = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(current_file))

def load_reference_shapes(folder_path):
    """Load reference shape contours from black and white images"""
    reference_shapes = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            label = os.path.splitext(filename)[0]
            img = cv2.imread(os.path.join(folder_path, filename), cv2.IMREAD_GRAYSCALE)
            _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                reference_shapes[label] = contours[0]
            else:
                print(f"No contour found in {filename}")
    return reference_shapes

def process_image(image_path, reference_shapes, counter):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Try both normal and inverted thresholds
    _, thresh_normal = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    _, thresh_inv = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Get contours for both thresholds
    contours_normal, _ = cv2.findContours(thresh_normal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_inv, _ = cv2.findContours(thresh_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Use whichever threshold found more contours
    contours = contours_normal if len(contours_normal) > len(contours_inv) else contours_inv
    
    # Filter small contours
    min_area = 200  # Adjust this value based on your image size
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
    print(f"Found {len(contours)} potential symbols")

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        best_match = None
        best_score = float('inf')

        for label, ref_cnt in reference_shapes.items():
            score = cv2.matchShapes(cnt, ref_cnt, cv2.CONTOURS_MATCH_I1, 0.0)
            if score < best_score:
                best_score = score
                best_match = label

        if best_match:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, best_match, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (255, 0, 0), 2)

    cv2.imwrite(f"UNIQoutput{counter}.jpg", img)
    cv2.destroyAllWindows()

def select_and_run(counter):
    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Select an image to analyze")
    if not image_path:
        print("No image selected.")
        return

    # Use fixed path relative to project root
    shapes_folder = os.path.join(get_project_root(), "ubec\shapes")
    if not os.path.exists(shapes_folder):
        print(f"Error: Shapes folder not found at {shapes_folder}")
        return

    reference_shapes = load_reference_shapes(shapes_folder)
    process_image(image_path, reference_shapes, counter)

if __name__ == "__main__":
    select_and_run(0)
