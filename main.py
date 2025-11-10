from typing import Callable
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, \
                            QWidget, \
                            QMainWindow, \
                            QPushButton, \
                            QVBoxLayout, \
                            QLineEdit
#
# Задание 
# 1. Метод половинного деления
# 2. Метод двух секущих

# Половинное деление
def HalfSection(a: float, b: float, f: Callable[[float], float], eps: float):
    if (f(a)*f(b) < 0):
        pass # Корней нет

    i: int = 0
    while 1:
        x0: float = (a + b) / 2
        i+=1

        if f(x0) == 0:
            break # Корней нет?
        
        if f(a) * f(x0) < 0:
            b = x0
        else:
            b = x0

        if abs(b - a) <= eps and f(x0) <= eps:
            break # Выход с выводом корня
    
# Метод двух секущих
# Метод двухшаговый - потому что на каждом шаге нужно 2 точки 
def DoubleSecant(a: float, b: float, f: Callable[[float], float], eps: float,
                                                                  i_max: int) -> float:
    i: int = 1
    x_prev: float = a
    x_crnt: float = b
    f_prev: float = f(x_prev)
    f_crnt: float 
    while i < i_max:
        f_crnt = f(x_crnt)
        x_new = x_crnt - (x_crnt - x_prev)/(f_crnt - f_prev)*f_crnt
        e:float = abs(x_new - x_crnt)

        if e < eps:
             break
        else:
            x_prev = x_crnt
            f_prev = f_crnt
            x_crnt = x_new
            i+=1
    return x_crnt


class MainWindow(QMainWindow):
    def set_plot(self, x:list[float], y:list[float]):
        self.plot_graph.plot(
            x,
            y,
            name = "ВычМат 1",
        )

    def __init__(self):
        super().__init__()

        # Temperature vs time plot
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setBackground("w")
        self.plot_graph.showGrid(x=True, y=True)

        button = QPushButton("TEST");
        self.input = QLineEdit()
        # connect text changed signal

        layout = QVBoxLayout()        
        layout.addWidget(self.plot_graph)
        layout.addWidget(button)
        layout.addWidget(self.input)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


f: Callable[[float], float] = lambda x: x*x*x + 10

app = QApplication([])
main = MainWindow()
time:list[float] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
temperature:list[float] = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
main.set_plot(time, temperature)
main.show()
app.exec()
