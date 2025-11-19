import collections.abc as t
from math import cos, isnan, sqrt
from scipy.optimize import root_scalar
from PyQt6.QtWidgets import QApplication
from compmathui import MainWindow


def main() -> None:
    app    = QApplication([])
    window = MainWindow()

    # Функция
    f: t.Callable[[float], float] = lambda x: \
            sqrt(x) - cos(0.374 + x) if x>=0 else float("nan")
    eps: float = 0.0001

    window.show()
    app   .exec()

if __name__ == "__main__":
    main()
