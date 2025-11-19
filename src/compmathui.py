import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QMainWindow, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QLineEdit, 
    QTableWidget, 
    QTableWidgetItem, 
    QDoubleValidator, 
    QHeaderView
)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._ui()
        self._layout()


    def _ui(self) -> None:
        # plot graph
        self.plot_graph: pg.PlotWidget = pg.PlotWidget()
        self.plot_graph.setBackground("w")
        self.plot_graph.showGrid(x=True, y=True)

        # status 
        self.status_container: QWidget = QWidget()
        self.status_label:QLabel = QLabel("Hi!")

        # input 
        self.buttons_container: QWidget = QWidget()
        self.update_button: QPushButton = QPushButton("Update");
        self.update_button.clicked.connect(self._update)

        self.a_input_label: QLabel = QLabel("a:")
        self.a_input: QLineEdit = QLineEdit()
        self.a_input.setValidator(QDoubleValidator(10e-15, 10e15, 2))

        self.b_input_label: QLabel = QLabel("b:")
        self.b_input: QLineEdit = QLineEdit()
        self.b_input.setValidator(QDoubleValidator(10e-15, 10e15, 2))

        self.eps_input_label: QLabel = QLabel("eps:")
        self.eps_input: QLineEdit = QLineEdit()
        self.eps_input.setValidator(QDoubleValidator(10e-15, 10e15, 2))

        self.max_iter_input_label: QLabel = QLabel("max_iter:")
        self.max_iter_input: QLineEdit = QLineEdit()
    
        # table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)  
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        # main 
        self.container: QWidget = QWidget()


    def _layout(self) -> None:
        # status 
        status_layout: QHBoxLayout = QHBoxLayout()
        status_layout.addWidget(self.status_label)

        self.status_container.setLayout(status_layout)
        # input
        buttonx_layout: QHBoxLayout = QHBoxLayout()
        buttonx_layout.addWidget(self.update_button) 

        buttonx_layout.addWidget(self.a_input_label) 
        buttonx_layout.addWidget(self.a_input)

        buttonx_layout.addWidget(self.b_input_label) 
        buttonx_layout.addWidget(self.b_input)

        buttonx_layout.addWidget(self.eps_input_label) 
        buttonx_layout.addWidget(self.eps_input)

        buttonx_layout.addWidget(self.max_iter_input_label) 
        buttonx_layout.addWidget(self.max_iter_input)

        self.buttons_container.setLayout(buttonx_layout)

        layout: QVBoxLayout = QVBoxLayout()        
        layout.addWidget(self.plot_graph)
        layout.addWidget(self.status_container)
        layout.addWidget(self.buttons_container)
        layout.addWidget(self.table_widget)

        self.container.setLayout(layout)
        self.setCentralWidget(self.container)


    def _update(self) -> None:
        eps:  float   =  self.eps_input.text()
        a:    float   =  self.a_input.text()
        b:    float   =  self.b_input.text()
        max_iter: int =  self.max_iter_input.text()

        # v: IterVisitor = IterVisitor()
        # f: Callable[[float], float] = lambda x: \
        #        sqrt(x) - cos(0.374 + x) if x>=0 else float("nan")

        # (r, x) = my_bisect(a, b, f, eps, v) 
        # if not r:
        #     self.status_label.setText("Root not find (")
        #     return
        #
        # self.status_label.setText(f"x={x}")
        #
        # t: list[tuple[int, float, float]] = v.get()

        # Updating Table
        # self.table_widget.setRowCount(len(t))
        # for i in range(len(t)):
        #     for j in range(3):
        #         self.table_widget.setItem(i, j, QTableWidgetItem(str(t[i][j])))
    
    def _update_a(self) -> None:
        pass

    def _update_b(self) -> None:
        pass

    def _set_plot(self,
                  x: list[float],
                  y: list[float]
                  ) -> None:
        self.plot_graph.plot(
            x,
            y,
            name = "",
        )
