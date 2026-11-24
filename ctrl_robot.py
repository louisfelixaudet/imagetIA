from ev_app import *
from robot import Robot
import param


class CtrlRobot(EvApp):
    def __init__(self, port_no):
        super().__init__(port_no)
        self.robot = Robot()

    def dispatch_event(self, ev):
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
