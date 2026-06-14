from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem,
    QLabel, QProgressBar
)
from scanner import PingScanner


class NetworkScannerUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ping Network Scanner")
        self.setGeometry(200, 200, 700, 400)

        self.layout = QVBoxLayout()

        self.subnet_input = QLineEdit()
        self.subnet_input.setPlaceholderText("Enter subnet (e.g., 192.168.1.0/24)")
        self.layout.addWidget(self.subnet_input)

        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        self.layout.addWidget(self.scan_button)

        self.stop_button = QPushButton("Stop Scan")
        self.stop_button.clicked.connect(self.stop_scan)
        self.layout.addWidget(self.stop_button)

        self.status_label = QLabel("Idle")
        self.layout.addWidget(self.status_label)

        self.progress = QProgressBar()
        self.layout.addWidget(self.progress)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["IP Address", "RTT (ms)"])
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.scanner = None
        self.row_count = 0

    def start_scan(self):
        subnet = self.subnet_input.text().strip()

        if not subnet:
            self.status_label.setText("Enter a subnet")
            return

        self.table.setRowCount(0)
        self.row_count = 0
        self.progress.setValue(0)

        self.status_label.setText("Scanning...")

        self.scanner = PingScanner(subnet)
        self.scanner.result_signal.connect(self.add_result)
        self.scanner.finished_signal.connect(self.scan_finished)
        self.scanner.start()

    def add_result(self, ip, rtt):
        self.table.insertRow(self.row_count)

        self.table.setItem(self.row_count, 0, QTableWidgetItem(ip))
        self.table.setItem(self.row_count, 1, QTableWidgetItem(str(rtt)))

        self.row_count += 1

    def scan_finished(self):
        self.status_label.setText("Scan Completed")
        self.progress.setValue(100)

    def stop_scan(self):
        if self.scanner:
            self.scanner.stop()
            self.status_label.setText("Stopped")