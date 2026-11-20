from lireImage import Camera
import cv2
import time

img_id = 0
nbImage = 25
print("------ choix fichier -------")
print("1. arreter")
print("2. continuer")
fichier = "arreter" if input("1 ou 2: ") == 1 else  "continuer"

for i in range(nbImage):
    image = Camera.capturer()
    cv2.imwrite(f"./image_rgb/{fichier}/image_{img_id}.png", image)
    time.sleep(4)
print("all 10 picture capture")