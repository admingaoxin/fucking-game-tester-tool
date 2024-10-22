import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QTextEdit, QLabel, QFileDialog


class ADBCommandExecutor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("选择命令集合：", self)
        layout.addWidget(self.label)

        self.comboBox = QComboBox(self)
        self.load_command_sets('commands.txt')  # 从文件加载命令集合
        layout.addWidget(self.comboBox)

        self.executeButton = QPushButton("执行命令", self)
        self.executeButton.clicked.connect(self.execute_commands)
        layout.addWidget(self.executeButton)

        self.outputText = QTextEdit(self)
        self.outputText.setReadOnly(True)
        layout.addWidget(self.outputText)

        self.setLayout(layout)
        self.setWindowTitle('ADB 命令执行器')
        self.setGeometry(300, 300, 400, 300)

    def load_command_sets(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith('#'):
                        self.comboBox.addItem(line[1:])  # 添加标识符到下拉框
        except FileNotFoundError:
            self.outputText.append(f"文件 {file_path} 未找到。")
        except Exception as e:
            self.outputText.append(f"发生错误: {e}")

    def execute_commands(self):
        set_identifier = self.comboBox.currentText()
        file_path = 'commands.txt'  # 这里可以使用 QFileDialog.getOpenFileName() 来选择文件
        self.outputText.clear()
        self.outputText.append(f"执行命令集合: {set_identifier}\n")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            commands = []
            collect = False
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    if line == f'#{set_identifier}':
                        collect = True
                    else:
                        collect = False
                elif collect and line:
                    commands.append(line)

            if not commands:
                self.outputText.append(f"未找到标识符 '{set_identifier}' 对应的命令集合。")
                return

            process = subprocess.Popen(['adb', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)

            for command in commands:
                process.stdin.write(command + '\n')

            process.stdin.close()

            output, error = process.communicate()

            if process.returncode == 0:
                self.outputText.append("命令执行成功，输出如下：")
                self.outputText.append(output)
            else:
                self.outputText.append("命令执行失败，错误信息如下：")
                self.outputText.append(error)

        except FileNotFoundError:
            self.outputText.append(f"文件 {file_path} 未找到。")
        except Exception as e:
            self.outputText.append(f"发生错误: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ADBCommandExecutor()
    ex.show()
    sys.exit(app.exec_())