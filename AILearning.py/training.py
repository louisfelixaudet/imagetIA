import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
import modele 
import torch.nn as nn
import matplotlib.pyplot as plt
import cv2
import numpy as np
from torchvision import transforms



IMAGE_DIR = "./image_rgb/" 
CHEMIN = "./pt_modele/kf2_modele.pt"
TAILLE_LOT = 32  
TAILLE_IMG = 128

image_transform = transforms.Compose([            # pipeline de transformation  
    transforms.Resize((TAILLE_IMG, TAILLE_IMG)),  # redimesionner l'image
    transforms.ToTensor()                         # représenter l'image à l'aide de Tensor
])

# Informe Pytorch du type de donnée et de emplacement
# Installe un pipeline de transformation
entrainement_dataset = datasets.ImageFolder(os.path.join(IMAGE_DIR, "entrainement"), 
                                            transform=image_transform)

# DataLoader retourne les images par lot de TAILLE_LOT
entrainement_loader = DataLoader(entrainement_dataset, 
                                 batch_size=TAILLE_LOT, shuffle=True)

LEARNING_RATE = 0.001	# Taux d’apprentissage
NUM_EPOCHS    = 10	    # Nombre d’itérations d'entraînement

# Vérifier la présence d'un processeur graphique GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

criterion = nn.CrossEntropyLoss()	    # Fonction de coût
optimizer = optim.Adam(modele.parameters(), lr=LEARNING_RATE)	# Descente de gradient kf2
modele.to(device)
modele.train()   # activer le modèle en mode entrainement
for epoch in range(NUM_EPOCHS):  # num_epochs itération de toutes les images
	total_loss, correct = 0, 0
	for images, labels in entrainement_loader:
		images, labels = images.to(device), labels.to(device)
		outputs = modele(images)
		loss = criterion(outputs, labels)
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()
		total_loss += loss.item()
		correct += (outputs.argmax(1) == labels).sum().item() # Nombre de prédictions correctes 
															  # dans un batch
	acc = 100 * correct / len(entrainement_loader.dataset)
	print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}, Accuracy: {acc:.2f}%")

# Sauvegarder uniquement les paramètres: 
torch.save(modele.state_dict(), CHEMIN)

# Charger uniquement les paramètres: 
modele.load_state_dict(torch.load(CHEMIN))




image = plt.imread("image_rgb/validation/continuer/image_122.png")
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
    output = modele(image_tensor)
    _, predicted = torch.max(output, 1) # max de la dimension 1
label = labels[predicted.item()] if predicted.item() < len(labels) else "?"
print(output, label)