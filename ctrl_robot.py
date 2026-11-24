from ev_app import *
from robot import Robot
import param
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
import modele as m
import torch.nn as nn
import matplotlib.pyplot as plt
import cv2
import numpy as np
from torchvision import transforms
from lireImage import Camera
import time
import os
import torch

CHEMIN = "../pt_modele/kf2_modele.pt"
TAILLE_LOT = 32  
TAILLE_IMG = 128
IMAGE_DIR = "../image_rgb/"

class CtrlRobot(EvApp):
    def __init__(self, port_no):
        super().__init__(port_no)
        self.robot = Robot()

    def predire_image(self, cam):
        m.modele.load_state_dict(torch.load(CHEMIN))
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        image = plt.imread(cam.capture())
        print(image.shape)
        plt.imshow(image, cmap='gray')
        plt.axis('off')

        labels =  [param.ARRETER, param.CONTINUER]  # en ordre alphabétique

        # Prétraitement de l’image

        image = cv2.resize(image, (TAILLE_IMG, TAILLE_IMG))

        image_tensor = torch.tensor(image.transpose(2, 0, 1)).float().unsqueeze(0) / 255.0

        image_tensor = image_tensor.to(device)

        with torch.no_grad():
                output = m.modele(image_tensor)
                _, predicted = torch.max(output, 1) # max de la dimension 1
        label = labels[predicted.item()] if predicted.item() < len(labels) else "?"
        return (output, label)

    def dispatch_event(self, ev):
        cam = Camera()
        cam.demarrer()

        if ev.type == 0:
            return

        donnee = ev.split()
        try:
            v = float(donnee[0]) if donnee and donnee[0] != "" else 0.0
        except ValueError:
            v = 0.0

        if ev.type == param.DROITE:
            self.robot.tournerDroite(v)
        elif ev.type == param.AVANCER:
            output, label = self.predire_image(cam)
            print(output, label)
            if label == param.ARRETER:
                self.robot.arreter()
            elif label == param.CONTINUER:
                self.robot.avancer(v)

        elif ev.type == param.GAUCHE:
            self.robot.tournerGauche(v)
        elif ev.type == param.RECULER:
            self.robot.reculer(v)
        elif ev.type == param.AUG_SPEED:
            print(f"augmente de {v}")
        elif ev.type == param.DIM_SPEED:
            print(f"diminue de {v}")
        elif ev.type == param.ARRET:
            self.robot.arreter()
        elif ev.type == param.STOP:
            self.robot.arreter()
            self.quitter_app()
        else:
            print("message invalide", ev)

    def quitter(self):
        try:
            self.robot.arreter()
        except Exception:
            pass
        print("Bye bye")


ctrl_robot = CtrlRobot(port_no=param.NUM_PORT)
ctrl_robot.run()
