import torch.nn as nn

NB_CLASSES = 2
modele = nn.Sequential(
    nn.Conv2d(3, 16, 3, padding=1),	# nb de couleurs (3), 16 filtres donc 16 images, kernel (3x3) 
    nn.ReLU(), # fonction d’activation Rectified Linear Unit
    nn.MaxPool2d(2), # maximum sur une fenêtre 2x2, réduction spatiale de 2 
    nn.Conv2d(16, 32, 3, padding=1), # 16 images , 32 filtres 3x3 donc sortie 32 images de 
    nn.ReLU(), # fonction d’activation Rectified Linear Unit
    nn.MaxPool2d(2), # maximum sur une fenêtre 2x2, réduction spatiale de 2 
    nn.Flatten(), # passe de 2D à 1D 
    nn.Linear(32 * 32 * 32, 128), # images 32x32 (128->64->32) x32 filtres réseau de neurones standards 32768 à 128
    nn.ReLU(),  # fonction d’activation Rectified Linear Unit
    nn.Linear(128, NB_CLASSES) # réseau de neurones standards 128 à num_classes
)