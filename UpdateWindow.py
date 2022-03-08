from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QListWidget, QListWidgetItem
import main


class UpdateWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Instance Variable Declarations
        self.table_list = None
        self.record_list = None
        # After records have been imported from the database, store them in record_cache
        # Keys are table names, values are data. This saves load time when switching between tables.
        self.record_cache = {}
        # End of Instance Variable Declarations

        self.setup_window()

    def setup_window(self):
        self.setGeometry(100, 300, 600, 700)
        self.setWindowTitle("Update Database Records")
        self.table_list = QComboBox(self)
        self.table_list.move(50, 20)
        self.table_list.resize(200, 25)
        self.record_list = QListWidget(self)
        self.record_list.move(50, 80)
        self.record_list.resize(500, 520)
        update_button = QPushButton("Update", self)
        update_button.clicked.connect(self.update_record)
        update_button.resize(update_button.sizeHint())
        update_button.move(50, 650)
        delete_button = QPushButton("Delete", self)
        delete_button.clicked.connect(self.delete_record)
        delete_button.resize(delete_button.sizeHint())
        delete_button.move(450, 650)
        self.show()

    def populate_list(self):
        current_table = self.table_list.currentText()
        records = self.record_cache.get(current_table)
        if records is None:
            db = main.open_db("im.db")
            records = main.query_entire_table(db[1], current_table)
            main.close_db(db[0])

        for record in records.values():
            fields = ""
            for field in record.values():
                fields += field + " --- "
            QListWidgetItem(fields, self.table_list)

    def update_record(self):
        print("placeholder")

    def delete_record(self):
        db = main.open_db("im.db")
        current_record = self.record_list.currentItem()

        # Records are in the list as a single string. This line uses some string manipulation to isolate the id
        record_id = current_record.text().split(" --- ")[0]

        main.delete_record(db[1], self.table_list.currentText, record_id)
        main.close_db(db[0])
