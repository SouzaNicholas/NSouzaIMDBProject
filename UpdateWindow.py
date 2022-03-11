from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QListWidget, QListWidgetItem

import UpdateDialog
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
        self.setGeometry(100, 300, 1400, 700)
        self.setWindowTitle("Update Database Records")
        self.table_list = QComboBox(self)
        self.table_list.move(50, 20)
        self.table_list.resize(200, 25)
        self.populate_table_list()
        self.table_list.currentIndexChanged.connect(self.populate_record_list)
        self.record_list = QListWidget(self)
        self.record_list.move(50, 80)
        self.record_list.resize(1300, 520)
        self.populate_record_list()
        update_button = QPushButton("Update", self)
        update_button.clicked.connect(self.update_record)
        update_button.resize(update_button.sizeHint())
        update_button.move(50, 650)
        delete_button = QPushButton("Delete", self)
        delete_button.clicked.connect(self.delete_record)
        delete_button.resize(delete_button.sizeHint())
        delete_button.move(1250, 650)
        self.show()

    def populate_table_list(self):
        tables = ["shows", "movies", "popularShows", "popularMovies", "ratings"]
        for table in tables:
            self.table_list.addItem(table)

    # Acts as a factory for items in the list of records. Records are checked against the
    # cache of records to save load times. Then values are concatenated into a single string.
    # I use string slicing to strip off excess formatting. It takes up less space than using
    # logic to prevent the extra " --- " from being put on in the first place.
    def populate_record_list(self):
        self.record_list.clear()
        current_table = self.table_list.currentText()
        records = self.record_cache.get(current_table)
        if records is None:
            db = main.open_db("im.db")
            records = main.query_entire_table(db[1], current_table)
            self.record_cache[current_table] = records
            main.close_db(db[0])

        for record in records:
            fields = ""
            for column in record.keys():
                fields += column + ": " + str(record[column]) + " --- "
            QListWidgetItem(fields[:-5], self.record_list)

    def update_record(self):
        if self.record_list.currentItem() is not None:
            update_form = UpdateDialog.UpdateDialog(self.convert_record_to_dict())
            update_form.exec()
            updated_record = update_form.record_data

            db = main.open_db("im.db")
            main.update_record(db[1], self.table_list.currentText(), updated_record)
            main.close_db(db[0])

    def delete_record(self):
        db = main.open_db("im.db")
        current_record = self.record_list.currentItem()

        # Records are in the list as a single string. This line uses some string manipulation to isolate the id
        record_id = current_record.text().split(" --- ")[0]

        main.delete_record(db[1], self.table_list.currentText, record_id)
        main.close_db(db[0])

    # Method assumes text is being taken directly from the QListWidget when formatting
    def convert_record_to_dict(self) -> dict:
        current_record = self.record_list.currentItem().text()
        formatted_record = {}
        record_text = current_record.split(" --- ")
        for field in record_text:
            pair = field.split(": ")
            formatted_record[pair[0]] = pair[1]
        return formatted_record
