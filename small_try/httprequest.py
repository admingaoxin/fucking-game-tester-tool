import sys
import asyncio
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QComboBox
from PyQt5.QtCore import Qt, pyqtSlot
import aiohttp
import logging

logging.basicConfig(filename='http_requests.log', level=logging.INFO,
                    format='%(asctime)s: %(levelname)s - %(message)s')

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

        self.send_count_input = QLineEdit (self)
        self.send_count_input.setPlaceholderText ('Enter number of requests to send')
        self.send_count_input.setValidator (QIntValidator ())  # 添加验证器确保输入的是整数

        self.body_input = QTextEdit(self)
        self.body_input.setPlaceholderText('Enter request body (for POST only)')

        self.send_btn = QPushButton('Send', self)
        self.send_btn.clicked.connect(self.send_request)

        # self.response_text = QTextEdit(self)
        # self.response_text.setReadOnly(True)

        layout.addWidget(self.url_input)
        layout.addWidget(self.method_combo)
        layout.addWidget(self.body_input)
        layout.addWidget(self.send_btn)
        # layout.addWidget(self.response_text)
        layout.addWidget (self.send_count_input)

        self.setLayout(layout)
    # ... initUI 方法保持不变 ...

    @pyqtSlot()  # 标记为Qt槽，确保在GUI线程中调用
    def send_request(self):
        url = self.url_input.text()
        method = self.method_combo.currentText()
        send_count = int(self.send_count_input.text()) if self.send_count_input.text() else 1
        asyncio.run(self.send_requests_async(url, method, send_count))


    async def send_requests_async(self, url, method, send_count):
        body = self.body_input.toPlainText().encode('utf-8') if method == 'POST' else None

        tasks = []
        if method == 'GET':
            tasks = [self.send_get_request_async(url) for _ in range(send_count)]
        elif method == 'POST':
            tasks = [self.send_post_request_async(url, body) for _ in range(send_count)]

        await asyncio.gather(*tasks)

    async def send_get_request_async(self, url):
        try:
            async with aiohttp.ClientSession () as session:
                async with session.get (url) as response:
                    text = await response.text ()
                    # 记录日志而不是更新GUI
                    logging.info (f"GET {url} Status Code: {response.status}")
                    logging.info (f"Response: {text[:10000]}...")
        except Exception as e:
            logging.error (f"GET {url} Error: {e}")

    async def send_post_request_async(self, url, body):
        headers = {'Content-Type': 'application/json'}
        try:
            async with aiohttp.ClientSession () as session:
                async with session.post (url, data=body, headers=headers) as response:
                    text = await response.text ()
                    # 在这里你可以决定如何处理响应，例如记录日志或更新GUI
                    logging.info (f"POST {url} Status Code: {response.status}")
                    logging.info (f"Response: {text[:10000]}...")
        except Exception as e:
            logging.error (f"POST {url} Error: {e}")

# ... 主程序保持不变 ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HttpRequester()
    ex.send_request ()
    ex.show()
    sys.exit(app.exec_())