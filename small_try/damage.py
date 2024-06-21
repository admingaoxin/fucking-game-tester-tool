from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
import sys

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.variables = {f'var{i}': 0.0 for i in range(1, 31)}
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.line_edits = {}
        for name in self.variables.keys():
            hbox = QHBoxLayout()

            label = QLabel(name, self)
            hbox.addWidget(label)

            line_edit = QLineEdit(self)
            self.line_edits[name] = line_edit
            line_edit.textChanged[str].connect(lambda text, name = name: self.update_var(name, text))
            hbox.addWidget(line_edit)

            vbox.addLayout(hbox)

        calc_button = QPushButton('Calculate', self)
        calc_button.clicked.connect(self.calculate)
        vbox.addWidget(calc_button)

        self.setLayout(vbox)
        self.setWindowTitle('My App')
        self.show()

    def update_var(self, name, text):
        try:
            self.variables[name] = float(text)
        except ValueError:
            pass  # 输入的不是一个有效的浮点数，忽略

    def calculate(self):
        # 在这里定义你的计算过程
        # 例如，我们可以计算所有变量的总和
        total = sum(self.variables.values())
        print(f'Total: {total}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())