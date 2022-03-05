from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QListWidget


class UpdateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()

    def setup_window(self):
        self.setGeometry(100, 300, 600, 700)
        self.setWindowTitle("Update Database Records")
        table_list = QComboBox(self)
        table_list.move(50, 20)
        table_list.resize(200, 25)
        record_list = QListWidget(self)
        record_list.move(50, 80)
        record_list.resize(500, 520)
        update_button = QPushButton("Update", self)
        update_button.clicked.connect(self.update_record)
        update_button.resize(update_button.sizeHint())
        update_button.move(50, 650)
        delete_button = QPushButton("Delete", self)
        delete_button.clicked.connect(self.delete_record)
        delete_button.resize(delete_button.sizeHint())
        delete_button.move(450, 650)
        self.show()

    def update_record(self):
        print("placeholder")

    def delete_record(self):
        print("placeholder")
