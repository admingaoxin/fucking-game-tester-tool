import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSlot

class CommandExecutor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.command_combo = QComboBox(self)
        self.load_commands()
        layout.addWidget(self.command_combo)

        self.execute_btn = QPushButton('Execute', self)
        self.execute_btn.clicked.connect(self.on_execute_button_clicked)
        layout.addWidget(self.execute_btn)

        self.logText = QTextEdit()
        self.logText.setReadOnly(True)
        layout.addWidget(self.logText)

        self.setLayout(layout)

    def load_commands(self):
        try:
            with open('commands.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if '；' in line:
                        comment, command = line.split('；', 1)
                        self.command_combo.addItem(comment.strip(), command.strip())
        except FileNotFoundError:
            self.logText.append("commands.txt 文件未找到。")

    @pyqtSlot()
    def on_execute_button_clicked(self):
        command = self.command_combo.currentData()
        if command:
            asyncio.run(self.execute_command_async(command))

    async def execute_command_async(self, command):
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # 逐行读取 stdout
            async for line in process.stdout:
                self.logText.append(f"Output: {line.decode('utf-8').strip()}")

            # 逐行读取 stderr
            async for line in process.stderr:
                self.logText.append(f"Error: {line.decode('utf-8').strip()}")

            await process.wait()
        except Exception as e:
            self.logText.append(f"执行命令时出错: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    executor = CommandExecutor()
    executor.show()
    sys.exit(app.exec_())