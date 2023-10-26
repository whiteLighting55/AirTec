import numpy as np
import cv2
import matplotlib.pyplot as plt


def triangular_mask(height, width):
    """
    Creates a triangular mask.
    :param height: height of the mask.
    :param width: width of the mask.
    :return: A boolean mask where True indicates the mask.
    """

    # Create a meshgrid for the coordinates
    ys, xs = np.ogrid[:height, :width]

    # Define the three vertices of the triangle (in this case an upright triangle centered in the image)
    left_vertex = [0,height]
    right_vertex = [width,height]
    top_vertex = [width // 2,height//3]

    # Using the Barycentric coordinate system to create a mask for the triangle
    detT = (top_vertex[1] - right_vertex[1]) * (left_vertex[0] - right_vertex[0]) + (
                right_vertex[0] - top_vertex[0]) * (left_vertex[1] - right_vertex[1])
    alpha = ((ys - right_vertex[1]) * (left_vertex[0] - right_vertex[0]) + (right_vertex[0] - xs) * (
                left_vertex[1] - right_vertex[1])) / detT
    beta = ((ys - left_vertex[1]) * (top_vertex[0] - left_vertex[0]) + (left_vertex[0] - xs) * (
                top_vertex[1] - left_vertex[1])) / detT
    gamma = 1 - alpha - beta

    # Masking where alpha, beta, and gamma are all within the range [0, 1] constitutes the triangle
    mask = (alpha >= 0) & (alpha <= 1) & (beta >= 0) & (beta <= 1) & (gamma >= 0) & (gamma <= 1)

    return mask

# Initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Couldn't open the camera.")
    exit()

while True:
    # Capture one frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read from the camera.")
        cap.release()
        exit()

    # Convert the frame from BGR (which is OpenCV's default) to RGB

    # Generate the mask
    height, width, channels = frame.shape
    mask = triangular_mask(height, width)

    # Apply the mask: where the mask is False, set the pixel value to 0
    frame[~mask] = 0

    # Display the masked image using matplotlib
    cv2.imshow("Imagen Enmascarada",frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
