from lireImage import Camera
import cv2
import time
import os

ID_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "id.txt")
try:
    with open(ID_FILE) as f:
        img_id = int(f.read().strip())
except (FileNotFoundError, ValueError):
    img_id = 0

nbImage = 10
print("------ choix fichier -------")
print("1. arreter")
print("2. continuer")
fichier = "arreter" if input("1 ou 2: ") == "1" else  "continuer"
cam = Camera()
cam.demarrer()

for i in range(nbImage):
    image = cam.capture()
    cv2.imshow("Frame", image)
    cv2.waitKey(1)
    cv2.imwrite(f"../image_rgb/validation/{fichier}/image_{img_id}.png", image)
    print("a picture have been taking...")
    time.sleep(4)
    img_id += 1

with open(ID_FILE, "w") as f:
    f.write(str(img_id))

print("all 10 picture have been captured")

