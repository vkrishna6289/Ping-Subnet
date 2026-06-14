from scapy.all import IP, ICMP, sr1
from PyQt5.QtCore import QThread, pyqtSignal
import ipaddress
import time


class PingScanner(QThread):
    result_signal = pyqtSignal(str, float)
    finished_signal = pyqtSignal()

    def __init__(self, subnet):
        super().__init__()
        self.subnet = subnet
        self.running = True

    def run(self):
        network = ipaddress.ip_network(self.subnet, strict=False)

        for ip in network.hosts():
            if not self.running:
                break

            target = str(ip)
            start = time.time()

            packet = IP(dst=target) / ICMP()

            reply = sr1(packet, timeout=1, verbose=0)

            if reply:
                rtt = (time.time() - start) * 1000
                self.result_signal.emit(target, round(rtt, 2))

        self.finished_signal.emit()

    def stop(self):
        self.running = False