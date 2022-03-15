from PyQt5.QtWidgets import QWidget, QComboBox
from pyqtgraph import PlotWidget, BarGraphItem

import main


class VisualizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.graph = None
        self.graph_list = None
        self.setup_window()

    def setup_window(self):
        self.setGeometry(100, 300, 600, 600)
        self.setWindowTitle("Visualize Data")

        self.graph = PlotWidget(self)
        self.graph.move(50, 50)
        self.graph.resize(500, 500)

        self.graph_list = QComboBox(self)
        self.graph_list.move(20, 20)
        self.graph_list.resize(200, 20)
        self.populate_graph_list()
        self.graph_list.currentIndexChanged.connect(self.reset_graph)

        self.show()

    def populate_graph_list(self):
        graphs = ["Moving Ranks", "Popular Movies in Top 250", "Popular Shows in Top 250"]
        for graph in graphs:
            self.graph_list.addItem(graph)
        self.reset_graph()

    def reset_graph(self):
        if self.graph_list.currentIndex() == 0:
            self.paint_moving_rank_graph()
        elif self.graph_list.currentIndex() == 1:
            self.paint_movie_crossover_graph()
        elif self.graph_list.currentIndex() == 2:
            self.paint_show_crossover_graph()

    def paint_moving_rank_graph(self):
        self.graph.clear()
        db = main.open_db("im.db")
        data = [main.total_shows_moving_up(db[1]), main.total_shows_moving_down(db[1]),
                main.total_movies_moving_up(db[1]), main.total_movies_moving_down(db[1])]
        main.close_db(db[0])
        self.graph.addItem(BarGraphItem(x=range(4), height=data, width=0.4))

    def paint_movie_crossover_graph(self):
        self.graph.clear()
        db = main.open_db("im.db")
        data = len(main.popular_movies_in_top(db[1]))
        main.close_db(db[0])
        self.graph.addItem(BarGraphItem(x=range(1), height=data, width=0.4))

    def paint_show_crossover_graph(self):
        self.graph.clear()
        db = main.open_db("im.db")
        data = len(main.popular_shows_in_top(db[1]))
        main.close_db(db[0])
        self.graph.addItem(BarGraphItem(x=range(1), height=data, width=0.4))
