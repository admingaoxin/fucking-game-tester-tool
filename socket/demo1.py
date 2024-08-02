import os
from scapy.all import *
import time
import optparse
import datetime
from PyQt5 import QtWidgets, QtGui, QtCore

nowtime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
print(nowtime)

# 回调打印函数
def PackCallBack(packet, hostIP, ui, writer):
    direction = "Outgoing" if packet[IP].src == hostIP else "Incoming"
    summary = "[%s] %s: %s:%s ----> %s:%s" % (TimeStamp2Time(packet.time), direction, packet[IP].src, packet.sport, packet[IP].dst, packet.dport)
    details = packet.show(dump=True)
    if Raw in packet:
        details += "\nProtocol Content: " + str(packet[Raw].load)
    ui.packet_received.emit(summary, details)
    writer.write(packet)

# 时间戳转换函数
def TimeStamp2Time(timeStamp):
    timeTmp = time.localtime(timeStamp)
    myTime = time.strftime("%Y-%m-%d %H:%M:%S", timeTmp)
    return myTime

class PacketSnifferUI(QtWidgets.QWidget):
    packet_received = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.packet_received.connect(self.add_packet)
        self.sniffer_thread = None

    def initUI(self):
        self.setWindowTitle('Packet Sniffer')
        self.setGeometry(100, 100, 800, 600)

        self.ipLabel = QtWidgets.QLabel('IP Address:', self)
        self.ipInput = QtWidgets.QLineEdit(self)
        self.ipInput.setText('39.98.196.51')

        self.startButton = QtWidgets.QPushButton('Start Sniffing', self)
        self.startButton.clicked.connect(self.toggle_sniffing)

        self.packetList = QtWidgets.QListWidget(self)
        self.packetDetails = QtWidgets.QTextEdit(self)
        self.packetDetails.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.ipLabel)
        layout.addWidget(self.ipInput)
        layout.addWidget(self.startButton)
        layout.addWidget(self.packetList)
        layout.addWidget(self.packetDetails)
        self.setLayout(layout)

        self.packetList.itemClicked.connect(self.display_packet_details)

    def toggle_sniffing(self):
        if self.sniffer_thread and self.sniffer_thread.isRunning():
            self.sniffer_thread.terminate()
            self.sniffer_thread = None
            self.startButton.setText('Start Sniffing')
        else:
            self.packetList.clear()
            self.packetDetails.clear()
            hostIP = self.ipInput.text()
            defFilter = "host " + hostIP
            fileName = f'{nowtime}.pcap'
            self.sniffer_thread = SnifferThread(defFilter, hostIP, self, fileName)
            self.sniffer_thread.start()
            self.startButton.setText('Stop Sniffing')

    def add_packet(self, summary, details):
        item = QtWidgets.QListWidgetItem(summary)
        item.setData(QtCore.Qt.UserRole, details)
        self.packetList.addItem(item)

    def display_packet_details(self, item):
        details = item.data(QtCore.Qt.UserRole)
        self.packetDetails.setPlainText(details)

class SnifferThread(QtCore.QThread):
    def __init__(self, filter, hostIP, ui, fileName):
        super().__init__()
        self.filter = filter
        self.hostIP = hostIP
        self.ui = ui
        self.fileName = fileName

    def run(self):
        writer = PcapWriter(self.fileName, append=True, sync=True)
        while True:
            packets = sniff(filter=self.filter, prn=lambda x: PackCallBack(x, self.hostIP, self.ui, writer), count=5)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = PacketSnifferUI()
    window.show()
    app.exec_()