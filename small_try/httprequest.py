import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QComboBox
from PyQt5.QtCore import Qt
import requests
import traceback
class HttpRequester(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('HTTP Requester')
        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Enter URL')

        self.method_combo = QComboBox(self)
        self.method_combo.addItem('GET')
        self.method_combo.addItem('POST')

        self.body_input = QTextEdit(self)
        self.body_input.setPlaceholderText('Enter request body (for POST only)')

        self.send_btn = QPushButton('Send', self)
        self.send_btn.clicked.connect(self.send_request)

        self.response_text = QTextEdit(self)
        self.response_text.setReadOnly(True)

        layout.addWidget(self.url_input)
        layout.addWidget(self.method_combo)
        layout.addWidget(self.body_input)
        layout.addWidget(self.send_btn)
        layout.addWidget(self.response_text)

        self.setLayout(layout)

    def send_request(self):
        url = self.url_input.text()
        method = self.method_combo.currentText()

        if method == 'GET':
            self.send_get_request(url)
        elif method == 'POST':
            body = self.body_input.toPlainText().encode('utf-8')
            print("Encoded body:", body) # Encode the body for POST requests
            self.send_post_request(url, body)


    def send_get_request(self, url):
        try:
            response = requests.get(url)
            # 只显示状态码
            self.response_text.setText(f"Status Code: {response.status_code}")
        except requests.RequestException as e:
            self.response_text.setText(f"Error: {e}")

    def send_post_request(self, url, body):
        headers = {'Content-Type': 'application/json'}  # 根据需要更改此内容类型
        try:
            # 确保body是字节串（如果需要）
            body_bytes = body.encode ('utf-8') if isinstance(body, str) else body
            print("Sending POST request to:", url)
            print("Body:",
                   body_bytes.decode('utf-8') if isinstance(body_bytes, bytes) else body_bytes)  # 仅用于调试，显示文本内容
            response = requests.post(url, data=body_bytes, headers=headers) #, headers=headers
            print("Response status code:", response.status_code)
            self.response_text.setText (response.text)
        except requests.RequestException as e:
            self.response_text.setText (f"Error: {e}")
            traceback.print_exc()  # 打印完整的堆栈跟踪
        except Exception as e:
            self.response_text.setText (f"Unexpected error: {e}")
            traceback.print_exc()  # 打印完整的堆栈跟踪



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HttpRequester()
    ex.show()
    sys.exit(app.exec_())