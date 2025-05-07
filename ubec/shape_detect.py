import os
from tkinter import filedialog, Tk
import cv2
import numpy as np
from db import DatabaseManager
from shape_detection import ImageProcessor

""" Main file for main feature """

class ShapeDetector:
    def __init__(self):
        self.db = DatabaseManager()
        self.processor = ImageProcessor()

    def get_project_root(self):
        current_file = os.path.abspath(__file__)
        return os.path.dirname(os.path.dirname(current_file))

    def run(self):
        root = Tk()
        root.withdraw()
        image_path = filedialog.askopenfilename(title="Select an image to analyze")
        if not image_path:
            print("No image selected.")
            return

        input_filename = os.path.basename(image_path)
        
        # Check if already processed
        existing = self.db.get_entry(input_filename)
        if existing:
            self._handle_existing_image(input_filename, existing[1])
            return

        # Process new image
        shapes_folder = os.path.join(self.get_project_root(), "ubec/shapes")
        if not os.path.exists(shapes_folder):
            print(f"Error: Shapes folder not found at {shapes_folder}")
            return

        self._process_new_image(image_path, shapes_folder)

    def _handle_existing_image(self, filename: str, image_bytes: bytes):
        print(f"Image {filename} was previously processed")
        output_path = os.path.join(self.get_project_root(), "saves", f"retrieved_{filename}")
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite(output_path, img)
        print(f"Retrieved image saved to: {output_path}")

    def _process_new_image(self, image_path: str, shapes_folder: str):
        reference_shapes = self.processor.load_reference_shapes(shapes_folder)
        processed_img = self.processor.process_image(image_path, reference_shapes)
        
        # Save processed image
        output_folder = os.path.join(self.get_project_root(), "saves")
        os.makedirs(output_folder, exist_ok=True)
        
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_folder, f"detected_{filename}")
        cv2.imwrite(output_path, processed_img)

        # Save to database
        _, img_encoded = cv2.imencode('.png', processed_img)
        self.db.create_entry(filename, img_encoded.tobytes())

if __name__ == "__main__":
    detector = ShapeDetector()
    detector.run()