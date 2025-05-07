import cv2 # OpenCV Library
import tkinter as tk
from tkinter import filedialog

def process_image(image_path: str) -> None:
    # Read the image
    image = cv2.imread(filename=image_path)

    # Convert to grayscale
    gray_image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
    
    # Preproccessing
    gray_image = cv2.GaussianBlur(src=gray_image, ksize=(5, 5), sigmaX=0)
    
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(3,3))
    gray_image = cv2.morphologyEx(src=gray_image, op=cv2.MORPH_CLOSE, kernel=kernel)
    
    # Setting threshold value to get new image (In simpler terms: this function checks every pixel, and depending on how
    # dark the pixel is, the threshold value will convert the pixel to either black or white (0 or 1)).
    _, thresh_image = cv2.threshold(src=gray_image, thresh=180, maxval=255, type=cv2.THRESH_BINARY)

    # Retrieving outer-edge coordinates in the new threshold image
    contours, _ = cv2.findContours(image=thresh_image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    # Iterating through each contour to retrieve coordinates of each shape
    for i, contour in enumerate(contours):
        if i == 0:
            continue

        # The 2 lines below this comment will approximate the shape we want. The reason being that in certain cases the
        # shape we want might have flaws or might be imperfect, and so, for example, if we have a rectangle with a
        # small piece missing, the program will still count it as a rectangle. The epsilon value will specify the
        # precision in which we approximate our shape.
        epsilon = 0.02*cv2.arcLength(curve=contour, closed=True)
        approx = cv2.approxPolyDP(curve=contour, epsilon=epsilon, closed=True)

        # Drawing the outer-edges onto the image
        cv2.drawContours(image=image, contours=[contour], contourIdx=0, color=(0, 0, 0), thickness=4)

        # Retrieving coordinates of the contour so that we can put text over the shape.
        x, y, w, h= cv2.boundingRect(array=approx)
        x_mid = int(x + (w/3)) # This is an estimation of where the middle of the shape is in terms of the x-axis.
        y_mid = int(y + (h/1.5)) # This is an estimation of where the middle of the shape is in terms of the y-axis.

        # Setting some variables which will be used to display text on the final image
        coords = (x_mid, y_mid)
        color = (0, 0, 0)
        font = cv2.FONT_HERSHEY_DUPLEX

        # This is the part where we actually guess which shape we have detected. The program will look at the amount of edges
        # the contour/shape has, and then based on that result the program will guess the shape (for example, if it has 3 edges
        # then the chances that the shape is a triangle are very good.)
        #
        # You can add more shapes if you want by checking more lenghts, but for the simplicity of this tutorial program I
        # have decided to only detect 5 shapes.
        if len(approx) == 3:
            cv2.putText(image, "Triangle", coords, font, 1, color, 1) # Text on the image
        elif len(approx) == 4:
            cv2.putText(image, "Quadrilateral", coords, font, 1, color, 1)
        elif len(approx) == 5:
            cv2.putText(image, "Pentagon", coords, font, 1, color, 1)
        elif len(approx) == 6:
            cv2.putText(image, "Hexagon", coords, font, 1, color, 1)

    # Display the frame
    cv2.imshow(winname="shapes_detected", mat=image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def select_image() -> None:
    # Hide the main Tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("All files", "*.*")
        ]
    )
    
    if file_path:
        process_image(file_path)

if __name__ == "__main__":
    select_image()