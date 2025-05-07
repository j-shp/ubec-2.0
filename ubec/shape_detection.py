import cv2
import numpy as np
import os
from typing import Dict, List

"""

Mainly Image Processing

"""
class ImageProcessor:
    def __init__(self, min_area: int = 200):
        self.min_area = min_area

    def load_reference_shapes(self, folder_path: str) -> Dict[str, np.ndarray]:
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

    def process_image(self, image_path: str, reference_shapes: Dict[str, np.ndarray]) -> np.ndarray:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        _, thresh_normal = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        _, thresh_inv = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        contours_normal, _ = cv2.findContours(thresh_normal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_inv, _ = cv2.findContours(thresh_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contours = contours_normal if len(contours_normal) > len(contours_inv) else contours_inv
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > self.min_area]
        
        return self._process_contours(img, contours, reference_shapes)

    def _process_contours(self, img: np.ndarray, contours: List[np.ndarray], 
                         reference_shapes: Dict[str, np.ndarray]) -> np.ndarray:
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            best_match = None
            best_score = float('inf')

            for label, ref_cnt in reference_shapes.items():
                score = cv2.matchShapes(cnt, ref_cnt, cv2.CONTOURS_MATCH_I1, 0.0)
                if score < best_score:
                    best_score = score
                    best_match = label

            if best_match and best_score < 0.1:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, f"{best_match}", 
                           (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (255, 0, 0), 1)

        return img