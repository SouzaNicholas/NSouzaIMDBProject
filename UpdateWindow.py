from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QListWidget


class UpdateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()

    # Initially used manual placement of elements, but I'm trying addrow for a neater look
    def setup_window(self):
        self.setGeometry(100, 100, 600, 900)
        self.setWindowTitle("Update Database Records")
        table_list = QComboBox(self)
        self.addrow(table_list)
        # table_list.move(50, 20)
        # table_list.resize(table_list.sizeHint())
        record_list = QListWidget(self)
        self.addrow(record_list)
        # record_list.move(50, 80)
        # record_list.resize()
        update_button = QPushButton("Update", self)
        update_button.clicked.connect(self.update_data)
        # update_button.resize(update_button.sizeHint())
        # update_button.move(50, 780)
        delete_button = QPushButton("Delete", self)
        delete_button.clicked.connect(self.delete_record)
        # delete_button.resize(delete_button.sizeHint())
        # delete_button.move(450, 780)
        self.addrow(update_button, delete_button)

    def update_record(self):
        print("placeholder")

    def delete_record(self):
        print("placeholder")
