from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

import UpdateWindow as UW
import VisualizationWindow as VW


class LaunchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()

    def setup_window(self):
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
        update_window = UW.UpdateWindow()
        print(self)  # Here to remove "could be static" style warning, not permanent

    def open_visualization_window(self):
        data_window = VW.VisualizationWindow()
        print(self)  # Here to remove "could be static" style warning, not permanent
