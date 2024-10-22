# encryption_decryption.py
import sys
import base64
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtGui import QFont
from cryptography.fernet import Fernet, InvalidToken
import qt_material
import hashlib


class EncryptDecryptApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('加密解密工具')
        self.resize(400, 600)

        layout = QVBoxLayout()

        self.key_label = QLabel('密钥:')
        self.key_label.setFont(QFont('Arial', 12))
        layout.addWidget(self.key_label)

        self.key_input = QLineEdit()
        self.key_input.setFont(QFont('Arial', 12))
        layout.addWidget(self.key_input)

        self.text_label = QLabel('输入文本:')
        self.text_label.setFont(QFont('Arial', 12))
        layout.addWidget(self.text_label)

        self.text_input = QTextEdit()
        self.text_input.setFont(QFont('Arial', 12))
        layout.addWidget(self.text_input)

        self.encrypted_label = QLabel('加密文本:')
        self.encrypted_label.setFont(QFont('Arial', 12))
        layout.addWidget(self.encrypted_label)

        self.encrypted_output = QTextEdit()
        self.encrypted_output.setFont(QFont('Arial', 12))
        self.encrypted_output.setReadOnly(True)
        layout.addWidget(self.encrypted_output)

        self.decrypted_label = QLabel('解密文本:')
        self.decrypted_label.setFont(QFont('Arial', 12))
        layout.addWidget(self.decrypted_label)

        self.decrypted_output = QTextEdit()
        self.decrypted_output.setFont(QFont('Arial', 12))
        self.decrypted_output.setReadOnly(True)
        layout.addWidget(self.decrypted_output)

        self.encrypt_button = QPushButton('加密')
        self.encrypt_button.setFont(QFont('Arial', 12))
        self.encrypt_button.clicked.connect(self.encrypt_text)
        layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('解密')
        self.decrypt_button.setFont(QFont('Arial', 12))
        self.decrypt_button.clicked.connect(self.decrypt_text)
        layout.addWidget(self.decrypt_button)

        self.setLayout(layout)

    def get_fernet_key(self, key):
        # 使用SHA-256哈希函数生成固定长度的密钥
        digest = hashlib.sha256(key.encode()).digest()
        return Fernet(base64.urlsafe_b64encode(digest[:32]))

    def encrypt_text(self):
        try:
            key = self.key_input.text()
            text = self.text_input.toPlainText().encode()
            fernet = self.get_fernet_key(key)
            encrypted_text = fernet.encrypt(text)
            self.encrypted_output.setPlainText(encrypted_text.decode())
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加密失败: {str(e)}")

    def decrypt_text(self):
        try:
            key = self.key_input.text()
            encrypted_text = self.text_input.toPlainText().encode()
            fernet = self.get_fernet_key(key)
            decrypted_text = fernet.decrypt(encrypted_text)
            self.decrypted_output.setPlainText(decrypted_text.decode())
        except InvalidToken:
            QMessageBox.critical(self, "错误", "解密失败: 无效的密钥或加密文本")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"解密失败: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt_material.apply_stylesheet(app, theme='light_blue_500.xml')
    ex = EncryptDecryptApp()
    ex.show()
    sys.exit(app.exec_())