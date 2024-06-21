import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("damage demo")
        self.custom_variables = {"damagebase": "基础值damagebase", "modifier": "修饰modifier", "attack": "和ndm同级的attack修饰"}  # 在这里定义你的变量名和文本框前的名字
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 创建数字文本框
        self.number_boxes = {}
        for variable_name, label_name in self.custom_variables.items():
            number_box = QLineEdit()

            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"{label_name}："))
            hbox.addWidget(number_box)

            layout.addLayout(hbox)
            self.number_boxes[variable_name] = number_box

        # 创建一个按钮
        button = QPushButton("计算")
        button.clicked.connect(self.calculate)
        layout.addWidget(button)

        # 创建一个标签用于显示结果
        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate(self):
        # 获取数字
        for name, number_box in self.number_boxes.items():
            setattr(self, name, float(number_box.text()))

        # 执行自定义的计算过程
        result = self.custom_calculation()

        # 显示结果
        self.result_label.setText(f"计算结果: {result}天")

    def custom_calculation(self):
        # 在这里编写你的自定义计算过程
        total = (self.damagebase *(1+ self.modifier)) *(1+ self.attack)
        return total

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())