import cv2
import numpy as np

img = cv2.imread("prova.jpg")
cv2.imshow("img intera", img)
rows, cols, _ = img.shape
print("Rows", rows)
print("Cols", cols)
# Cut image
cv2.imshow("img intera", img)
cut_image = img[426: 853, 0: 1280]
cv2.imshow("cam",cut_image)
cv2.imshow("img intera", img)
k=cv2.waitKey(0)