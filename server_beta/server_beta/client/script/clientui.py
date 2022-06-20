from PyQt5 import QtWidgets
from pubdefines import MSGQUEUE_SEND, MSGQUEUE_RECV, CallManagerFunc, DELAY_TIME

import net.clientnetpack as clientnetpack
import sys

class CClientUI(QtWidgets.QDialog):
	def __init__(self):
		super(CClientUI, self).__init__()
		self.lineedit = QtWidgets.QLineEdit()
		self.btn = QtWidgets.QPushButton("ensure")
		self.btn.clicked.connect(self.sendmsg)
		self.layout = QtWidgets.QHBoxLayout()
		self.layout.addWidget(self.lineedit)
		self.layout.addWidget(self.btn)
		self.setLayout(self.layout)
		self.resize(300, 300)

	def sendmsg(self):
		text = self.lineedit.text()
		oSend = clientnetpack.PacketPrepare(0x02)
		clientnetpack.PacketAddS(text, oSend)
		clientnetpack.PacketSend(oSend)

def main():
	app = QtWidgets.QApplication(sys.argv)
	demo = CClientUI()
	demo.show()
	sys.exit(app.exec_())