from PyQt5.QtWidgets import QWidget


class VisualizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()

    def setup_window(self):
        self.setGeometry(100, 100, 900, 900)
        self.setWindowTitle("Visualize Data")
        self.show()
