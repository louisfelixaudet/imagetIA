from lireImage import Camera

image = camera.capturer()
img_id += 1
cv2.imwrite(f"./image_rgb/image_{img_id}.png", image)