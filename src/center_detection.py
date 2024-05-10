# Import the necessary packages
import argparse
import imutils
import cv2

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# Load the image, convert it to grayscale, blur it slightly,
# and threshold it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# Output the processed image
cv2.imwrite(args["image"] + f"-thresholded.jpg", thresh)

# Find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Loop over the contours
# ESTO LO COPIE ASI DE INTERNET PERO EN REALIDAD NOSOTROS TENDRIAMOS UN SOLO CONTORNO POR IMAGEN (IDEALMENTE)
i = 1
for c in cnts:
    # Compute the center of the contour
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # Draw the contour and center of the shape on the image
    cv2.drawContours(image, [c], -1, (0, 0, 255), 8)
    cv2.circle(image, (cX, cY), 10, (0, 0, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 0, 255), 8)

    # Save the image
    cv2.imwrite(args["image"] + f"-processed_contour" + str(i) + ".jpg", image)
    i = i + 1