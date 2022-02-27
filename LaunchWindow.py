from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

import UpdateWindow as uw
import VisualizationWindow as vw


class LaunchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("ImDb API Query System")
        self.setGeometry(100, 100, 350, 200)
        prompt = QLabel(self)
        prompt.setText("Would you like to update records or visualize data?")
        prompt.move(20, 20)
        prompt.resize(prompt.sizeHint())
        update_button = QPushButton("Update Data", self)
        update_button.clicked.connect(self.open_update_window)
        update_button.resize(update_button.sizeHint())
        update_button.move(50, 80)
        visualization_button = QPushButton("Visualize Data", self)
        visualization_button.clicked.connect(self.open_visualization_window)
        visualization_button.resize(visualization_button.sizeHint())
        visualization_button.move(200, 80)
        self.show()

    def open_update_window(self):
        update_window = uw.UpdateWindow()
        print(self)  # Here to remove "could be static" style warning, not permanent

    def open_visualization_window(self):
        data_window = vw.VisualizationWindow()
        print(self)  # Here to remove "could be static" style warning, not permanent
