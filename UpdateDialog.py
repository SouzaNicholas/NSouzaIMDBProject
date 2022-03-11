from PyQt5.QtWidgets import QDialog


class UpdateDialog(QDialog):
    def __init__(self, record_data: dict):
        super().__init__()
        self.record_data = record_data
        self.setup_window()

    def setup_window(self):
        print()
