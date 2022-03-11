from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QFormLayout


class UpdateDialog(QDialog):
    def __init__(self, record_data: dict):
        super().__init__()
        self.record_data = record_data
        self.field_labels = []
        self.field_line_edits = []
        self.setup_window()

    def setup_window(self):
        self.setGeometry(100, 300, 800, 700)
        self.setWindowTitle("Update Record")
        layout = QFormLayout(self)
        for column in self.record_data.keys():
            label = QLabel()
            label.setText(column)
            line_edit = QLineEdit(self.record_data[column])
            self.field_labels.append(label)
            self.field_line_edits.append(line_edit)
            layout.addRow(label, line_edit)

