import collections.abc as t
import math

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
              f: t.Callable[[float], float],
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
              f: t.Callable[[float], float],
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

        if math.isnan(f_crnt) or math.isnan(f_prev):
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
