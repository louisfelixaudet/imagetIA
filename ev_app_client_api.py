import socket
import struct

TAILLE_MSG = 256
TAILLE_MSG_TOT = TAILLE_MSG + 4  # + ev_ty (entier 4 octets)
MSG_PACK_FORMAT = f"!I {TAILLE_MSG}s"

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def gen_ev_externe(ip_addr, port_no, ev_ty, *args):
    try:
        ev_ty = int(ev_ty)
        ev_data = [str(d) for d in args]
        ev_data = ";".join(ev_data)
        ev_data = ev_data.encode("utf-8")
        msg = struct.pack(MSG_PACK_FORMAT, ev_ty, ev_data)
        client_sock.sendto(msg, (ip_addr, port_no))
    except ValueError:
        print(f"ev_ty doit-être un entier -> {ev_ty}")
        raise
