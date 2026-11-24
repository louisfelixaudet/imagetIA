from ev_app_client_api import *
import keyboard
import param

MOVE_KEYS = {
    "q": param.GAUCHE,
    "w": param.AVANCER,
    "e": param.DROITE,
    "s": param.RECULER,
}

DEFAULT_POWER = {
    param.GAUCHE: 0.7,
    param.AVANCER: 0.4,
    param.DROITE: 0.7,
    param.RECULER: 0.6,
}


class telecom:
    def __init__(self, port=param.NUM_PORT):
        self.port = port
        self.run = True
        self.power = 0.0
        self.directAct = 0

    def StopHandler(self, code):
        if code == param.ARRET:
            self.power = 0.0
            self.directAct = 0
        if code == param.STOP:
            print("Program has been stop")
            self.run = False
            self.power = 0.0
            self.directAct = 0

    def _any_move_held(self):
        return any(keyboard.is_pressed(k) for k in MOVE_KEYS)

    def _apply_move(self, code):
        self.directAct = code
        if code in (param.GAUCHE, param.DROITE):
            self.power = DEFAULT_POWER[code]
        elif self.power == 0:
            self.power = DEFAULT_POWER[code]
        self.SendMSG(code)

    def _stop_motion(self):
        self.StopHandler(param.ARRET)
        self.SendMSG(param.ARRET)

    def SendMSG(self, move):
        gen_ev_externe(param.IP_ADRESS, self.port, move, self.power)

    def handle_event(self, event):
        key = event.name
        down = event.event_type == keyboard.KEY_DOWN

        if not down:
            if key in MOVE_KEYS and not self._any_move_held():
                self._stop_motion()
            return

        if key == "x":
            self.StopHandler(param.STOP)
            self.SendMSG(param.STOP)
            return
        if key in ("space", " "):
            self._stop_motion()
            return
        if key == ".":
            if self.directAct in (param.AVANCER, param.RECULER):
                self.power = max(0.0, min(1.0, self.power + 0.05))
                self.SendMSG(self.directAct)
                print(self.power)
            return
        if key == ",":
            if self.directAct in (param.AVANCER, param.RECULER):
                self.power = max(0.0, min(1.0, self.power - 0.05))
                self.SendMSG(self.directAct)
                print(self.power)
            return
        if key in MOVE_KEYS:
            self._apply_move(MOVE_KEYS[key])
            print(self.power, key)
            return

        print("tapper une touche valide")


telecommande = telecom()
print("Telecommande: q=gauche  w=avancer  e=droite  s=reculer")
print("Relacher = arret.  ./, = vitesse  espace=arret  x=quitter")
print(f"Envoi vers {param.IP_ADRESS}:{telecommande.port}")
while telecommande.run:
    telecommande.handle_event(keyboard.read_event())
