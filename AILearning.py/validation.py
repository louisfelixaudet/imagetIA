import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
import modele as m
import torch.nn as nn
import matplotlib.pyplot as plt
import cv2
import numpy as np
from torchvision import transforms

CHEMIN = "../pt_modele/kf2_modele.pt"
TAILLE_LOT = 32  
TAILLE_IMG = 128
IMAGE_DIR = "../image_rgb/"

m.modele.load_state_dict(torch.load(CHEMIN))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

image = plt.imread("../image_rgb/entrainement/arreter/image_22.png")
print(image.shape)
plt.imshow(image, cmap='gray')
plt.axis('off')
	
labels =  ['arreter', 'continuer']  # en ordre alphabétique
    
# Prétraitement de l’image

image = cv2.resize(image, (TAILLE_IMG, TAILLE_IMG))

# image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB) # Peut-être pas nécessaire
   
# Permutation des axes Hauteur, Largeur, Canal en CHL 
# Unsqueeze ajoute une dimension pour le numéro du batch (batch, C, H, L)
# Diviser par 255 pour nomaliser les valeurs des couleur BGR
image_tensor = torch.tensor(image.transpose(2, 0, 1)).float().unsqueeze(0) / 255.0

image_tensor = image_tensor.to(device)

with torch.no_grad():
    output = m.modele(image_tensor)
    _, predicted = torch.max(output, 1) # max de la dimension 1
label = labels[predicted.item()] if predicted.item() < len(labels) else "?"
print(output, label)