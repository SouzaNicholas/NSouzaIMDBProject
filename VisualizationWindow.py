from PyQt5.QtWidgets import QWidget
from pyqtgraph import PlotWidget, BarGraphItem

import main


class VisualizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.graph = None
        self.setup_window()

    def setup_window(self):
        self.setGeometry(100, 300, 800, 800)
        self.setWindowTitle("Visualize Data")
        self.graph = PlotWidget(self)
        self.graph.move(200, 200)
        self.graph.resize(500, 500)
        self.paint_graph()
        self.show()

    def paint_graph(self):
        db = main.open_db("im.db")
        data = [main.total_shows_moving_up(db[1]), main.total_shows_moving_down(db[1]),
                main.total_movies_moving_up(db[1]), main.total_movies_moving_down(db[1])]
        main.close_db(db[0])
        self.graph.addItem(BarGraphItem(x=range(4), height=data, width=0.4))
