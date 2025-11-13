import pyqtgraph as pg

from typing import Callable, Optional
from math import cos, isnan, sqrt
from scipy.optimize import root_scalar
from PyQt6.QtWidgets import \
                            QApplication, \
                            QWidget, \
                            QMainWindow, \
                            QPushButton, \
                            QVBoxLayout, \
                            QHBoxLayout, \
                            QLabel, \
                            QLineEdit, \
                            QTableWidget, \
                            QTableWidgetItem, \
                            QDoubleValidator, \
                            QHeaderView

# Задание 
# 1. Метод половинного деления
# 2. Метод двух секущих

class IterVisitor():
    def __init__(self) -> None:
        self.total: list[tuple[
                int,   # Номер итерации
                float, # current x 
                float  # f(x)
            ]] = []

    def add(self, iter: tuple[int, float, float]) -> None:
        self.total.append(iter)

    def get(self) -> list[tuple[int, float, float]]: 
        return self.total


# Половинное деление
def my_bisect(a: float,
              b: float,
              f: Callable[[float], float],
              eps: float,
              vis: IterVisitor
              ) -> tuple[bool, float]:
    if f(a)*f(b) >= 0:
        return (False, 0) # Возможно корней нет

    i: int = 0
    while 1:
        x0 = (a + b) / 2
        i+=1
        fx: float = f(x0)

        vis.add((i, x0, fx))

        if fx == 0:
            return (True, x0)
        
        if f(a) * fx < 0:
            b = x0
        else:
            a = x0

        if abs(b - a) <= eps and fx <= eps:
            return (True, x0)

    return (False, 0)
    
# Метод двух секущих
# Метод двухшаговый - потому что на каждом шаге нужно 2 точки 
def my_secant(a: float,
              b: float,
              f: Callable[[float], float],
              eps: float,
              i_max: int,
              vis: IterVisitor
                 ) -> tuple[bool, float]:
    i: int = 1
    x_prev: float = a
    x_crnt: float = b
    f_prev: float = f(x_prev)
    f_crnt: float = 0

    while i < i_max:
        f_crnt = f(x_crnt)
        
        if f_crnt == f_prev:
            return (False, x_crnt) # Деление на ноль

        if isnan(f_crnt) or isnan(f_prev):
            return (False, x_crnt) 

        x_new = x_crnt - (x_crnt - x_prev) / (f_crnt - f_prev) * f_crnt
        e: float = abs(x_new - x_crnt)

        vis.add((i, x_new, f_crnt))

        if e < eps:
             break
        else:
            x_prev = x_crnt
            f_prev = f_crnt
            x_crnt = x_new
            i+=1

    return (True, x_crnt)


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

        v: IterVisitor = IterVisitor()
        f: Callable[[float], float] = lambda x: \
               sqrt(x) - cos(0.374 + x) if x>=0 else float("nan")

        (r, x) = my_bisect(a, b, f, eps, v) 
        if not r:
            self.status_label.setText("Root not find (")
            return

        self.status_label.setText(f"x={x}")

        t: list[tuple[int, float, float]] = v.get()

        # Updating Table
        self.table_widget.setRowCount(len(t))
        for i in range(len(t)):
            for j in range(3):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(t[i][j])))
    
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


def main() -> None:
    app    = QApplication([])
    window = MainWindow()

    # Функция
    f: Callable[[float], float] = lambda x: \
            sqrt(x) - cos(0.374 + x) if x>=0 else float("nan")
    eps: float = 0.0001

    window.show()
    app   .exec()

if __name__ == "__main__":
    main()
